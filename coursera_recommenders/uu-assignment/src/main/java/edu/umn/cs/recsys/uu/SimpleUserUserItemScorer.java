package edu.umn.cs.recsys.uu;

import java.lang.Math;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

import org.grouplens.lenskit.basic.AbstractItemScorer;
import org.grouplens.lenskit.data.dao.ItemEventDAO;
import org.grouplens.lenskit.data.dao.UserEventDAO;
import org.grouplens.lenskit.data.event.Rating;
import org.grouplens.lenskit.data.history.History;
import org.grouplens.lenskit.data.history.RatingVectorUserHistorySummarizer;
import org.grouplens.lenskit.data.history.UserHistory;
import org.grouplens.lenskit.vectors.MutableSparseVector;
import org.grouplens.lenskit.vectors.SparseVector;
import org.grouplens.lenskit.vectors.VectorEntry;

import it.unimi.dsi.fastutil.longs.LongSet;

import org.javatuples.Triplet;

import javax.annotation.Nonnull;
import javax.inject.Inject;

/**
 * User-user item scorer.
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class SimpleUserUserItemScorer extends AbstractItemScorer {
    private final UserEventDAO userDao;
    private final ItemEventDAO itemDao;

    @Inject
    public SimpleUserUserItemScorer(UserEventDAO udao, ItemEventDAO idao) {
        userDao = udao;
        itemDao = idao;
    }

    @Override
    public void score(long user, @Nonnull MutableSparseVector scores) {
        //  Score items for this user using user-user collaborative filtering

        // get ratings for current user
        MutableSparseVector userVector =
                getUserRatingVector(user).mutableCopy();
        // calculate user ratings mean
        Double userMean = userVector.mean();
        // mean center the ratings vector
        addToAllExistingValues(userVector, -userMean);

        // This is the loop structure to iterate over items to score
        for (VectorEntry e: scores.fast(VectorEntry.State.EITHER)) {

            // 1. Calculate similarity with all other users
            // Prepare container for calculated tuple of
            //     <similarity, -otherUser, meanCenteredItemRating>
            // Minus before otherUser id ensures that when reverse sorting
            // by similarity ties will be broken by lower user id
            List<Triplet<Double,Long,Double>> data =
                    new ArrayList<Triplet<Double,Long,Double>>();

            // Get all users that rated particular item
            LongSet users = itemDao.getUsersForItem(e.getKey());

            for (Long otherUser: users) {
                // skip current user
                if (otherUser == user) continue;

                // for each user get their ratings vector
                MutableSparseVector otherVector =
                        getUserRatingVector(otherUser).mutableCopy();
                // calculate mean
                Double otherMean = otherVector.mean();
                // and mean-center the ratings vector
                addToAllExistingValues(otherVector, -otherMean);

                // now, calculate a cosine similarity
                Double similarity = (
                        userVector.dot(otherVector)
                        / (userVector.norm() * otherVector.norm())
                );

                // skip if similarity is NaN
                if (similarity.isNaN()) continue;

                // add calculated stuff to a list
                data.add(Triplet.with(
                        similarity,
                        -otherUser,  // to break ties when reverse-sorting
                        otherVector.get(e.getKey())  // meanCenteredItemRating
                ));
            }

            // 2. Get top 30 users and stuff calculated for them
            Collections.sort(data, Collections.reverseOrder());
            data = data.subList(0, 30);

            /* optional debug to be sure everything works just fine
            System.out.format(
                    "\nData for user %d and item %d:\n",
                    user, e.getKey());
            for (Triplet<Double,Long,Double> quartet: data) {
                System.out.format("%s\n", quartet);
            }
            */

            // 3. Calculate score for an item
            Double dividend = 0.0;
            Double divisor = 0.0;
            for (Triplet<Double,Long,Double> quartet: data) {
                Double sim = quartet.getValue0();
                Double meanCenteredItemRating = quartet.getValue2();
                dividend += sim * meanCenteredItemRating;
                divisor += Math.abs(sim);
            }
            Double score = userMean + dividend / divisor;

            // store score in output vector
            scores.set(e.getKey(), score);
        }
    }

    /**
     * Get a user's rating vector.
     * @param user The user ID.
     * @return The rating vector.
     */
    private SparseVector getUserRatingVector(long user) {
        UserHistory<Rating> history =
                userDao.getEventsForUser(user, Rating.class);
        if (history == null) {
            history = History.forUser(user);
        }
        return RatingVectorUserHistorySummarizer.makeRatingVector(history);
    }

    /**
     * Add a number to all existing values in a SparseVector
     * @param ratings The ratings SparseVector
     * @param number The number that will be added
     */
    private void addToAllExistingValues(
            MutableSparseVector vector, Double number) {
        for (VectorEntry e: vector.fast()) {
            vector.set(e.getKey(), e.getValue() + number);
        }
    }
}
