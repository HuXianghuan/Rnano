<?php
header("Content-Type: application/json");

// 检查文件上传
$fileInfo = null;
if (isset($_FILES['sirna_file']) && $_FILES['sirna_file']['error'] === UPLOAD_ERR_OK) {
    $fileInfo = [
        "name" => $_FILES['sirna_file']['name'],
        "size" => $_FILES['sirna_file']['size'],
        "type" => $_FILES['sirna_file']['type'],
        "tmp_name" => $_FILES['sirna_file']['tmp_name']
    ];
} else {
    $fileInfo = "No file uploaded or upload error";
}

// 获取 POST 参数
$params = $_POST;

// 输出 JSON，方便调试
echo json_encode([
    "status" => "ok",
    "received_file" => $fileInfo,
    "received_params" => $params
], JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE);
