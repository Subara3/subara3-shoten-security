<?php require __DIR__ . '/../app/config.php';
$err = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $st = mysqli_prepare(db(), "SELECT id, name FROM members WHERE email=? AND password=? AND status='active'");
    $pw = md5($_POST['password']);
    mysqli_stmt_bind_param($st, 'ss', $_POST['email'], $pw);
    mysqli_stmt_execute($st);
    $row = mysqli_fetch_assoc(mysqli_stmt_get_result($st));
    if ($row) { $_SESSION['member'] = $row; header('Location: index.php'); exit; }
    $err = 'メールアドレスかパスワードが違います';
}
?><!doctype html><meta charset="utf-8"><title>会員ログイン</title>
<h1>会員ログイン</h1><p><?= h($err) ?></p>
<form method="post"><input name="email"><input name="password" type="password"><button>ログイン</button></form>
