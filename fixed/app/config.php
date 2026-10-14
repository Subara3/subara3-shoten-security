<?php
// 公開ディレクトリの外に置く。DBのパスワードは環境変数から読む
define('DB_HOST', 'db');
define('DB_USER', 'shop');
define('DB_NAME', 'shop');
define('SHOP_NAME', 'すばら３商店');

header_remove('X-Powered-By');   // .htaccess の Header unset では消えなかった（ロリポップで確認）

function db() {
    static $db = null;
    if ($db === null) {
        $db = mysqli_connect(DB_HOST, DB_USER, getenv('SHOP_DB_PASS'), DB_NAME);
        mysqli_set_charset($db, 'utf8mb4');
    }
    return $db;
}
function h($s) { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

function audit($admin, $action, $detail = '') {
    $st = mysqli_prepare(db(), 'INSERT INTO admin_audit (actor, action, detail, ip, at) VALUES (?, ?, ?, ?, NOW())');
    mysqli_stmt_bind_param($st, 'ssss', $admin, $action, $detail, $_SERVER['REMOTE_ADDR']);
    mysqli_stmt_execute($st);
}

session_set_cookie_params(['httponly' => true, 'samesite' => 'Lax', 'secure' => !empty($_SERVER['HTTPS'])]);
session_start();
