-- 持ち出されたのは 2019-04-01 時点のバックアップ。その時点で店が持っていたものを数える
SELECT 'members'   AS t, COUNT(*) AS rows_at_2019_04_01 FROM members WHERE created_at < '2019-04-01'
UNION ALL SELECT 'orders',          COUNT(*) FROM orders          WHERE ordered_at < '2019-04-01'
UNION ALL SELECT 'order_cards_old', COUNT(*) FROM order_cards_old WHERE created_at < '2019-04-01'
UNION ALL SELECT 'admins',          COUNT(*) FROM admins          WHERE created_at < '2019-04-01';
