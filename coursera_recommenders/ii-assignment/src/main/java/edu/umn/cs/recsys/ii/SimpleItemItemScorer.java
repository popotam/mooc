package edu.umn.cs.recsys.ii;

import org.grouplens.lenskit.basic.AbstractItemScorer;
import org.grouplens.lenskit.data.dao.UserEventDAO;
import org.grouplens.lenskit.data.event.Rating;
import org.grouplens.lenskit.data.history.History;
import org.grouplens.lenskit.data.history.RatingVectorUserHistorySummarizer;
import org.grouplens.lenskit.data.history.UserHistory;
import org.grouplens.lenskit.knn.NeighborhoodSize;
import org.grouplens.lenskit.scored.ScoredId;
import org.grouplens.lenskit.vectors.MutableSparseVector;
import org.grouplens.lenskit.vectors.SparseVector;
import org.grouplens.lenskit.vectors.VectorEntry;

import javax.annotation.Nonnull;
import javax.inject.Inject;
import java.util.List;

/**
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class SimpleItemItemScorer extends AbstractItemScorer {
    private final SimpleItemItemModel model;
    private final UserEventDAO userEvents;
    private final int neighborhoodSize;

    @Inject
    public SimpleItemItemScorer(SimpleItemItemModel m, UserEventDAO dao,
                                @NeighborhoodSize int nnbrs) {
        model = m;
        userEvents = dao;
        neighborhoodSize = nnbrs;
    }

    /**
     * Score items for a user.
     * @param user The user ID.
     * @param scores The score vector.  Its key domain is the items to score, and the scores
     *               (rating predictions) should be written back to this vector.
     */
    @Override
    public void score(long user, @Nonnull MutableSparseVector scores) {
        SparseVector ratings = getUserRatingVector(user);
        double avg_rating = ratings.sum() / ratings.size();

        for (VectorEntry e: scores.fast(VectorEntry.State.EITHER)) {
            long item = e.getKey();
            List<ScoredId> neighbors = model.getNeighbors(item);
            // TODO Score this item and save the score into scores
            double score = 0.0;
            double weight = 0.0;
            long count = 0;
            for (ScoredId neighbor: neighbors) {
                if (neighbor.getId() == item) {
                    //System.out.format("SELF ");
                    continue;
                }
                //System.out.format("%s ", count);
                if (ratings.containsKey(neighbor.getId())) {
                    //System.out.format("(%s) ", neighbor.getScore());
                    score += (ratings.get(neighbor.getId()) - avg_rating) * neighbor.getScore();
                    weight += neighbor.getScore();
                    count++;
                }
                if (count >= neighborhoodSize) {
                    break;
                }
            }
            score /= weight;
            score += avg_rating;
            //System.out.format("\nScore: %s\n", score);
            scores.set(e, score);
        }
    }

    /**
     * Get a user's ratings.
     * @param user The user ID.
     * @return The ratings to retrieve.
     */
    private SparseVector getUserRatingVector(long user) {
        UserHistory<Rating> history = userEvents.getEventsForUser(user, Rating.class);
        if (history == null) {
            history = History.forUser(user);
        }

        return RatingVectorUserHistorySummarizer.makeRatingVector(history);
    }
}
