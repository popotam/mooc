SELECT sum(count) FROM frequency WHERE term = 'washington' OR term = 'taxes' OR term='treasury' GROUP BY docid ORDER BY sum(count) DESC LIMIT 1;
