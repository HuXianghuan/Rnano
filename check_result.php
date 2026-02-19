<?php
header("Content-Type: application/json");

$taskId = $_GET['taskId'] ?? '';
$file = __DIR__ . "/tasks/$taskId.json";

if (!$taskId || !file_exists($file)) {
    echo json_encode(["status"=>"error","message"=>"Task not found"]);
    exit;
}

$data = json_decode(file_get_contents($file), true);

// 如果 JSON 中没有 status，就认为任务完成
if (!isset($data['status']) || $data['status'] !== 'running') {
    echo json_encode($data);
} else {
    echo json_encode(["status"=>"running"]);
}
