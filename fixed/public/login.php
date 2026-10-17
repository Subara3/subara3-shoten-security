<?php require __DIR__ . '/../app/config.php';
$err = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = (string)($_POST['email'] ?? '');
    $pass  = (string)($_POST['password'] ?? '');
    $st = mysqli_prepare(db(), "SELECT id, name, password FROM members WHERE email=? AND status='active'");
    mysqli_stmt_bind_param($st, 's', $email);
    mysqli_stmt_execute($st);
    $row = mysqli_fetch_assoc(mysqli_stmt_get_result($st));
    $ok = 0;
    if ($row) {
        if (password_verify($pass, $row['password'])) {
            $ok = 1;
        } elseif (strlen($row['password']) === 32 && hash_equals($row['password'], md5($pass))) {
            // 旧形式（塩なしMD5）のまま残っている人は、ログインできた時点で作り直す
            $ok = 1;
            $new = password_hash($pass, PASSWORD_DEFAULT);
            $up = mysqli_prepare(db(), 'UPDATE members SET password=? WHERE id=?');
            mysqli_stmt_bind_param($up, 'si', $new, $row['id']);
            mysqli_stmt_execute($up);
        }
    }
    if ($ok) {
        session_regenerate_id(true);
        $_SESSION['member'] = ['id' => $row['id'], 'name' => $row['name']];
        header('Location: index.php'); exit;
    }
    $err = 'メールアドレスかパスワードが違います';
}
?><!doctype html><meta charset="utf-8"><title>会員ログイン</title>
<h1>会員ログイン</h1><p><?= h($err) ?></p>
<form method="post"><input name="email"><input name="password" type="password"><button>ログイン</button></form>
