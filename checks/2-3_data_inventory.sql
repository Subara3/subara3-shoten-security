-- IPA 2-3：保有データの再点検（不要な情報は持たない）
SELECT status, COUNT(*) AS members, MIN(created_at) AS oldest FROM members GROUP BY status;

SELECT YEAR(withdrawn_at) AS withdrawn_year, COUNT(*) AS still_with_address
FROM members WHERE status = 'withdrawn' AND address <> '' GROUP BY withdrawn_year ORDER BY withdrawn_year;

SELECT COUNT(*) AS orders, MIN(ordered_at) AS oldest,
       SUM(ordered_at < '2019-04-01') AS older_than_7y FROM orders;

SELECT COUNT(*) AS card_rows, MIN(created_at) AS oldest, MAX(created_at) AS newest FROM order_cards_old;
