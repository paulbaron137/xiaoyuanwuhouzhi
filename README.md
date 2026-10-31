# 校园物候志 · gameV7

像素校园物候观察游戏，基于 **Phaser 3.88.2**，纯前端单文件（`index.html`）。

## 功能一览
- 大地图探索 + 掩码碰撞（WASD / 点击移动）
- 注册/登录、物种图鉴（38 鸟 + 10 植物）、物种身份证（编号 WMU-xx-xxxx）
- 三类物候标点（花讯/鸟讯/鸟撞）、**鸟随机移动**（每 20 秒换位置并提示）
- AI 识鸟（DeepSeek 视觉模型 `deepseek-flash`，多循环识别）
- 文化+植物打卡点（7 个）、**留言弹幕看板**（打卡点留言 + 弹幕飘屏 + 右下留言板）
- 鸟撞守护数据**弹幕流转**
- 鸟叫声播放（4 种鸟，`assets/sounds/`）
- 移动端适配（触屏点击移动 + 响应式布局）

## 本地运行
双击 `index.html` 即可；但 **AI 识鸟** 需要本地 HTTP 服务器（避免跨域限制）：

```bash
npx serve -l 5173 .
# 或
python -m http.server 5173
```

然后浏览器打开 `http://localhost:5173`。

## 部署到 Vercel
1. 把本目录推到 GitHub（含 `package.json` / `vercel.json` / `.gitignore`）；
2. 到 [vercel.com](https://vercel.com) → **Add New Project** → 导入该 GitHub 仓库；
3. 框架预设选 **Other**，构建命令留空、输出目录留空（Vercel 自动识别 `index.html`）；
4. 点 Deploy 即可。

> 注意：`CFG.DEEPSEEK_API_KEY` 目前明文写在前端，仅适合演示。上线请改为后端代理（key 放服务端）。

## 目录
```
index.html         游戏主文件（含全部逻辑）
phaser.min.js      Phaser 3.88.2
assets.js          全部贴图（base64 内嵌）
assets/sounds/     鸟叫声（mp3）
data/              数据库副本（只读参考，不参与运行）
package.json       部署元信息
vercel.json        Vercel 配置
README.md          本文档
```
