#!/usr/bin/env node
/** Agent-readable local control surface. JSON on stdout; errors on stderr. */
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { evaluateJob, handoffJob, initJob } from './lib.mjs';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const HELP = `建筑 3D 拆解流水线（本地控制台，无网络调用）

node pipeline/cli.mjs init --id <slug> --building <name> [--location <place>] [--era <period>]
node pipeline/cli.mjs status <id>    输出当前阶段、各门禁、阻塞和文件哈希（JSON）
node pipeline/cli.mjs handoff <id>   输出按工位排序的操作提示（Markdown）
node pipeline/cli.mjs verify <id>    重新验证；仅 READY_FOR_USER_REVIEW 返回 0
node pipeline/cli.mjs help

init 不覆盖已有任务。所有引用限 jobs/<id>/ 或 artifacts/ 内的真实本地文件。
TITMAS 可信连接器尚未实现；视频最高为 PREVIEW_ONLY，verify 返回 1。
格式：pipeline/CLI.md；机器合同：pipeline/schemas/contract.schema.json。
退出码：0=命令成功；1=verify 门禁未通过；2=参数/文件错误。
`;

function options(args) {
  const accepted = new Set(['id', 'building', 'location', 'era']);
  const values = {};
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i]?.startsWith('--') ? args[i].slice(2) : '';
    if (!accepted.has(key) || Object.hasOwn(values, key) || !args[i + 1] || args[i + 1].startsWith('--')) throw new Error(`Invalid, duplicated or missing option: ${args[i] ?? ''}`);
    values[key] = args[i + 1];
  }
  return values;
}

try {
  const [command = 'help', ...args] = process.argv.slice(2);
  if (['help', '--help', '-h'].includes(command)) process.stdout.write(HELP);
  else if (command === 'init') process.stdout.write(`${JSON.stringify(initJob(root, options(args)), null, 2)}\n`);
  else if (['status', 'verify', 'handoff'].includes(command)) {
    if (args.length !== 1) throw new Error(`${command} requires exactly one job id.`);
    if (command === 'handoff') process.stdout.write(handoffJob(root, args[0]));
    else {
      const result = evaluateJob(root, args[0]);
      process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
      if (command === 'verify' && !result.ready_for_user_review) process.exitCode = 1;
    }
  } else throw new Error(`Unknown command: ${command}. Run: node pipeline/cli.mjs help`);
} catch (error) {
  process.stderr.write(`${JSON.stringify({ error: error.message })}\n`);
  process.exitCode = 2;
}
