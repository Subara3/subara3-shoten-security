-- IPA 2-3 / 3：不要な情報は持たない
-- ※インシデント調査の対象になっているので、調査会社が控えを取り終えてから実行する

-- 2018年5月まで自前で持っていたカード情報。今は決済代行会社が持つので、店に置く理由がない
DROP TABLE order_cards_old;

-- 退会者の個人情報は消す（会員番号・状態・日付だけ残す）
UPDATE members
   SET email = CONCAT('withdrawn-', id, '@invalid'), password = '', name = '', zip = '',
       address = '', tel = '', birthday = NULL
 WHERE status = 'withdrawn';

-- 注文は帳簿として7年残すが、お届け先は7年を過ぎたら消す
UPDATE orders SET ship_name = '', ship_address = '', ship_tel = ''
 WHERE ordered_at < DATE_SUB('2026-10-14', INTERVAL 7 YEAR);

SELECT status, COUNT(*) AS members, SUM(address <> '') AS with_address FROM members GROUP BY status;
SELECT COUNT(*) AS orders, SUM(ship_address <> '') AS with_address,
       SUM(ordered_at < DATE_SUB('2026-10-14', INTERVAL 7 YEAR)) AS older_than_7y FROM orders;
SHOW TABLES;
