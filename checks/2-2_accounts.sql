-- IPA 2-2：作成した覚えのないアカウント、無効化されているはずのアカウント
SELECT login, role, active, note, created_at, last_login,
       DATEDIFF('2026-10-14', last_login) AS days_since_login
FROM admins ORDER BY created_at;

-- 管理画面へのログイン成功を、接続元ごとに
SELECT login, ip, COUNT(*) AS ok, MIN(at) AS first, MAX(at) AS last
FROM admin_login_log WHERE success = 1 GROUP BY login, ip ORDER BY first;

-- ログイン失敗を日ごとに
SELECT DATE(at) AS day, COUNT(*) AS failures, COUNT(DISTINCT ip) AS ips
FROM admin_login_log WHERE success = 0 GROUP BY DATE(at) ORDER BY day;
