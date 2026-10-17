# 树木的博客

使用 Hexo 和 Butterfly，发布到 https://blog.shumu.xin 。

## 本地预览

```sh
npm ci
npm run server
```

## 发布文章

在 `source/_posts/` 编写文章，相关图片放入 `source/`。

```sh
git add source
git commit -m "docs: publish new post"
git push origin main
```

推送到 `main` 后，GitHub Actions 自动构建并发布 GitHub Pages。
Pull request 只验证构建，不发布。也可以在 Actions 页面手动运行工作流。
部署失败时查看 Actions 日志；需要回退时，撤销有问题的提交并推送。

## 域名设置

GitHub 仓库 Settings → Pages 的发布来源为 GitHub Actions，
Custom domain 为 `blog.shumu.xin`，启用 Enforce HTTPS。
域名 DNS 的 `blog` CNAME 指向 `shumunet.github.io`。
更换域名时，同时修改 `_config.yml` 的 `url`、`source/CNAME`、
工作流中的域名验证，以及 GitHub Pages 和 DNS 设置。

本仓库为公开仓库：删除文章不会自动清除 Git 提交历史。
