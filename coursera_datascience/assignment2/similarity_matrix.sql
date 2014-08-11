SELECT sum(similarity) FROM (
	select A.docid as docid1, B.docid as docid2, sum(A.count * B.count) as similarity
	        from frequency as A, frequency as B
		where A.docid < B.docid AND A.term = B.term
			AND A.docid='10080_txt_crude' AND B.docid='17035_txt_earn'
	        group by A.term, B.term
	)
WHERE docid1='10080_txt_crude' AND docid2='17035_txt_earn'
GROUP BY docid1, docid2;
