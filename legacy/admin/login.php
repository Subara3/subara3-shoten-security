<?php require '../config.php';
$err = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $st = mysqli_prepare(db(), 'SELECT * FROM admins WHERE login=? AND password=? AND active=1');
    $pw = md5($_POST['password']);
    mysqli_stmt_bind_param($st, 'ss', $_POST['login'], $pw);
    mysqli_stmt_execute($st);
    $row = mysqli_fetch_assoc(mysqli_stmt_get_result($st));
    $ok = $row ? 1 : 0;
    $log = mysqli_prepare(db(), 'INSERT INTO admin_login_log (login, ip, success, at) VALUES (?, ?, ?, NOW())');
    mysqli_stmt_bind_param($log, 'ssi', $_POST['login'], $_SERVER['REMOTE_ADDR'], $ok);
    mysqli_stmt_execute($log);
    if ($row) {
        $_SESSION['admin'] = $row;
        mysqli_query(db(), 'UPDATE admins SET last_login=NOW() WHERE id=' . (int)$row['id']);
        header('Location: index.php'); exit;
    }
    $err = 'ログインできません';
}
?><!doctype html><meta charset="utf-8"><title>管理画面</title>
<h1>すばら３商店 管理画面</h1><p><?= h($err) ?></p>
<form method="post"><input name="login"><input name="password" type="password"><button>ログイン</button></form>
