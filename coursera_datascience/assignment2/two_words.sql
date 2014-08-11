SELECT count(*) FROM (
	SELECT docid, count(docid) FROM frequency WHERE term='transactions' OR term='world' GROUP BY docid HAVING count(docid) > 1
);

-- alternativelly:
SELECT count(*) FROM (
	SELECT f1.docid FROM (SELECT docid FROM frequency WHERE term='transactions') f1 JOIN (SELECT docid FROM frequency WHERE term='world') f2 ON f1.docid = f2.docid;
);
