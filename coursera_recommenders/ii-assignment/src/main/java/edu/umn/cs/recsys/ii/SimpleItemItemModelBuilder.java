package edu.umn.cs.recsys.ii;

import com.google.common.collect.ImmutableMap;
import com.google.common.collect.Ordering;
import com.google.common.primitives.Doubles;

import it.unimi.dsi.fastutil.longs.LongSet;
import it.unimi.dsi.fastutil.longs.LongSortedSet;

import org.grouplens.lenskit.collections.LongUtils;
import org.grouplens.lenskit.core.Transient;
import org.grouplens.lenskit.cursors.Cursor;
import org.grouplens.lenskit.data.dao.ItemDAO;
import org.grouplens.lenskit.data.dao.UserEventDAO;
import org.grouplens.lenskit.data.event.Event;
import org.grouplens.lenskit.data.history.RatingVectorUserHistorySummarizer;
import org.grouplens.lenskit.data.history.UserHistory;
import org.grouplens.lenskit.scored.ScoredId;
import org.grouplens.lenskit.scored.ScoredIdListBuilder;
import org.grouplens.lenskit.scored.ScoredIds;
import org.grouplens.lenskit.vectors.ImmutableSparseVector;
import org.grouplens.lenskit.vectors.MutableSparseVector;
import org.grouplens.lenskit.vectors.SparseVector;
import org.grouplens.lenskit.vectors.VectorEntry;
import org.grouplens.lenskit.vectors.similarity.CosineVectorSimilarity;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.inject.Inject;
import javax.inject.Provider;

import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * @author <a href="http://www.grouplens.org">GroupLens Research</a>
 */
public class SimpleItemItemModelBuilder implements Provider<SimpleItemItemModel> {
    private final ItemDAO itemDao;
    private final UserEventDAO userEventDao;
    private static final Logger logger = LoggerFactory.getLogger(SimpleItemItemModelBuilder.class);;

    @Inject
    public SimpleItemItemModelBuilder(@Transient ItemDAO idao,
                                      @Transient UserEventDAO uedao) {
        itemDao = idao;
        userEventDao = uedao;
    }

    @Override
    public SimpleItemItemModel get() {
        // Get the transposed rating matrix
        // This gives us a map of item IDs to those items' rating vectors
        Map<Long, ImmutableSparseVector> itemVectors = getItemVectors();

        // Get all items - you might find this useful
        LongSortedSet items = LongUtils.packedSet(itemVectors.keySet());
        // Map items to vectors of item similarities
        Map<Long,MutableSparseVector> itemSimilarities = new HashMap<Long, MutableSparseVector>();

        // TODO Compute the similarities between each pair of items
        // It will need to be in a map of longs to lists of Scored IDs to store in the model
        CosineVectorSimilarity cosineSimilarity = new CosineVectorSimilarity();

        for (long item: items) {
            MutableSparseVector simVector = MutableSparseVector.create(items);
            ImmutableSparseVector itemVector = itemVectors.get(item);
            //System.out.format("simVector: %s\n", simVector);
            //System.out.format("itemVector: %s\n", itemVector);
            for (long other: items) {
                //System.out.format("iter: %s other: %s\n", item, other);
                ImmutableSparseVector otherVector = itemVectors.get(other);
                //System.out.format("otherVector: %s\n", otherVector);
                double sim = cosineSimilarity.similarity(itemVector, otherVector);
                simVector.set(other, sim);
            }
            itemSimilarities.put(item, simVector);
        }
        
        Map<Long,List<ScoredId>> model = new HashMap<Long,List<ScoredId>>();
        for (Map.Entry<Long,MutableSparseVector> itemEntry: itemSimilarities.entrySet()) {
            ScoredIdListBuilder builder = new ScoredIdListBuilder(itemEntry.getValue().size());
            for (VectorEntry simEntry: itemEntry.getValue()) {
                if (simEntry.getValue() > 0.0) {
                    builder.add(simEntry.getKey(), simEntry.getValue());
                }
            }
            model.put(itemEntry.getKey(), builder.sort(new HighScoreOrder()).finish());
            //System.out.format("%s: %s\n", itemEntry.getKey(), model.get(itemEntry.getKey()));
        }
        
        return new SimpleItemItemModel(model);
    }

    private static final class HighScoreOrder extends Ordering<ScoredId> {
        @Override
        public int compare(ScoredId left, ScoredId right) {
            return -Doubles.compare(left.getScore(), right.getScore());
        }
    }

    /**
     * Load the data into memory, indexed by item.
     * @return A map from item IDs to item rating vectors. Each vector contains users' ratings for
     * the item, keyed by user ID.
     */
    public Map<Long,ImmutableSparseVector> getItemVectors() {
        // set up storage for building each item's rating vector
        LongSet items = itemDao.getItemIds();
        // map items to maps from users to ratings
        Map<Long,Map<Long,Double>> itemData = new HashMap<Long, Map<Long, Double>>();
        for (long item: items) {
            itemData.put(item, new HashMap<Long, Double>());
        }
        // itemData should now contain a map to accumulate the ratings of each item
        
        // stream over all user events
        Cursor<UserHistory<Event>> stream = userEventDao.streamEventsByUser();
        try {
            for (UserHistory<Event> evt: stream) {
                MutableSparseVector vector = RatingVectorUserHistorySummarizer.makeRatingVector(evt).mutableCopy();
                // vector is now the user's rating vector
                // TODO Normalize this vector and store the ratings in the item data
                double avg_rating = vector.sum() / vector.size();
                vector.add(-avg_rating);
                for (VectorEntry rating: vector) {
                    itemData.get(rating.getKey()).put(evt.getUserId(), rating.getValue());
                }
            }
        } finally {
            stream.close();
        }

        // This loop converts our temporary item storage to a map of item vectors
        Map<Long,ImmutableSparseVector> itemVectors = new HashMap<Long, ImmutableSparseVector>();
        for (Map.Entry<Long,Map<Long,Double>> entry: itemData.entrySet()) {
            MutableSparseVector vec = MutableSparseVector.create(entry.getValue());
            itemVectors.put(entry.getKey(), vec.immutable());
        }
        return itemVectors;
    }
}
