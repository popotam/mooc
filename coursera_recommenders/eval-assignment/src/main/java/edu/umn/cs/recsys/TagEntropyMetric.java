package edu.umn.cs.recsys;

import java.util.ArrayList;
import java.util.HashSet;

import com.google.common.collect.ImmutableList;
import edu.umn.cs.recsys.dao.ItemTagDAO;
import org.grouplens.lenskit.core.LenskitRecommender;
import org.grouplens.lenskit.eval.algorithm.AlgorithmInstance;
import org.grouplens.lenskit.eval.data.traintest.TTDataSet;
import org.grouplens.lenskit.eval.metrics.AbstractTestUserMetric;
import org.grouplens.lenskit.eval.metrics.TestUserMetricAccumulator;
import org.grouplens.lenskit.eval.metrics.topn.ItemSelectors;
import org.grouplens.lenskit.eval.traintest.TestUser;
import org.grouplens.lenskit.scored.ScoredId;
import org.grouplens.lenskit.vectors.MutableSparseVector;
import org.grouplens.lenskit.vectors.VectorEntry;

import javax.annotation.Nonnull;
import java.util.List;

/**
 * A metric that measures the tag entropy of the recommended items.
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class TagEntropyMetric extends AbstractTestUserMetric {
    private final int listSize;
    private final List<String> columns;

    /**
     * Construct a new tag entropy metric.
     * 
     * @param nitems The number of items to request.
     */
    public TagEntropyMetric(int nitems) {
        listSize = nitems;
        // initialize column labels with list length
        columns = ImmutableList.of(String.format("TagEntropy@%d", nitems));
    }

    /**
     * Make a metric accumulator.  Metrics operate with <em>accumulators</em>, which are created
     * for each algorithm and data set.  The accumulator measures each user's output, and
     * accumulates the results into a global statistic for the whole evaluation.
     *
     * @param algorithm The algorithm being tested.
     * @param data The data set being tested with.
     * @return An accumulator for analyzing this algorithm and data set.
     */
    @Override
    public TestUserMetricAccumulator makeAccumulator(AlgorithmInstance algorithm, TTDataSet data) {
        return new TagEntropyAccumulator();
    }

    /**
     * Return the labels for the (global) columns returned by this metric.
     * @return The labels for the global columns.
     */
    @Override
    public List<String> getColumnLabels() {
        return columns;
    }

    /**
     * Return the lables for the per-user columns returned by this metric.
     */
    @Override
    public List<String> getUserColumnLabels() {
        // per-user and global have the same fields, they just differ in aggregation.
        return columns;
    }


    private class TagEntropyAccumulator implements TestUserMetricAccumulator {
        private double totalEntropy = 0;
        private int userCount = 0;

        /**
         * Evaluate a single test user's recommendations or predictions.
         * @param testUser The user's recommendation result.
         * @return The values for the per-user columns.
         */
        @Nonnull
        @Override
        public Object[] evaluate(TestUser testUser) {
            List<ScoredId> recommendations =
                    testUser.getRecommendations(listSize,
                                                ItemSelectors.allItems(),
                                                ItemSelectors.trainingItems());
            if (recommendations == null) {
                return new Object[1];
            }
            LenskitRecommender lkrec = (LenskitRecommender) testUser.getRecommender();
            ItemTagDAO tagDAO = lkrec.get(ItemTagDAO.class);
            TagVocabulary vocab = lkrec.get(TagVocabulary.class);

            double entropy = 0;

            // TODO Implement the entropy metric
            //System.out.format("\nStarting enthropy!\n");
            // build a list of all tags in all recommendations
            HashSet<Long> tagList = new HashSet<Long>();
            List<HashSet<Long>> moviesTags = new ArrayList<HashSet<Long>>();
            for (ScoredId recommendation: recommendations) {
                HashSet<Long> movieTags = new HashSet<Long>();
                for (String tag : tagDAO.getItemTags(recommendation.getId())) {
                    long tagId = vocab.getTagId(tag);
                    tagList.add(tagId);
                    movieTags.add(tagId);
                }
                moviesTags.add(movieTags);
            }
            //System.out.format("Total tags: %s\n", tagList.size());
            // calculate probability for each tag
            for (Long tagId: tagList) {
                double probability = 0.0;
                for (HashSet<Long> movieTags: moviesTags) {
                    if (movieTags.contains(tagId)) {
                        probability += 1.0 / (recommendations.size() * movieTags.size());
                    }
                }
                if (probability > 0.0) {
                    entropy += -probability * (Math.log(probability) / Math.log(2));
                }
            }
            //System.out.format("Enthropy: %s\n", entropy);

            totalEntropy += entropy;
            userCount += 1;
            return new Object[]{entropy};
        }

        /**
         * Get the final aggregate results.  This is called after all users have been evaluated, and
         * returns the values for the columns in the global output.
         *
         * @return The final, aggregated columns.
         */
        @Nonnull
        @Override
        public Object[] finalResults() {
            // return a single field, the average entropy
            return new Object[]{totalEntropy / userCount};
        }
    }
}
