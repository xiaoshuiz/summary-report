# TypeScript Native Previews 详细解读

**来源:** [Announcing TypeScript Native Previews - Microsoft Dev Blogs](https://devblogs.microsoft.com/typescript/announcing-typescript-native-previews/)

微软在 TypeScript 的性能和开发体验上迈出了重要一步，正式宣布了 **TypeScript Native Previews**。这意味着 TypeScript 编译器和相关工具正在被移植到原生代码，旨在提供更快的编译速度和更高效的开发流程。

## 核心发布内容

*   **原生编译器预览版 (`tsgo`)**:
    *   通过 npm 包 `@typescript/native-preview` 提供。安装后会得到一个名为 `tsgo` 的可执行文件，其功能与现有的 `tsc` 类似。
    *   **安装命令**: `npm install -D @typescript/native-preview`
    *   **运行示例**: `npx tsgo --project ./src/tsconfig.json`
    *   **目标**: `tsgo` 最终会更名为 `tsc` 并整合到主要的 `typescript` 包中，目前独立存在是为了方便测试。
*   **VS Code 原生预览扩展**:
    *   名为 "TypeScript (Native Preview)" 的扩展已在 Visual Studio Marketplace 上架。
    *   **注意**: 此扩展尚处早期，它会**默认让位于 VS Code 内置的 TypeScript 扩展**。用户需要手动启用它。
    *   **启用方式**:
        1.  通过 VS Code 命令面板运行 "TypeScript Native Preview: Enable (Experimental)"。
        2.  或在设置 UI 中勾选 "TypeScript > Experimental: Use Tsgo"。
        3.  或在 JSON 配置文件中添加 `"typescript.experimental.useTsgo": true`。

## 显著的性能提升："Corsa" 项目

*   **10 倍速度提升**: 将 TypeScript 编译器和工具集移植到原生代码（使用的是 **Go 语言**），并结合**共享内存并行与并发技术**，带来了平均 **10 倍的编译速度提升**。
*   **内部代号**: 这个原生移植项目代号为 "**Corsa**"，最终将成为 **TypeScript 7**。作为对比，当前基于 JavaScript 的稳定版 TypeScript (如 TS 5.8) 被非正式称为 "Strada"。
*   **实例**: 对 Sentry 代码库的测试显示，使用 `tsgo` (Corsa) 进行类型检查的时间从原先 `tsc` (Strada) 的 **超过 1 分钟大幅缩减至不足 7 秒**。

## 功能进展与细节

*   **更全面的类型检查支持**:
    *   大部分类型检查器的核心功能已经完成移植。
    *   **JSX 类型检查**: 原生预览版现已支持对 JSX 表达式的类型检查。之前的版本仅能解析 JSX 但不进行类型检查。
    *   **JavaScript 类型检查 (JSDoc)**: 支持通过 JSDoc 注释对 `.js` 文件进行类型检查。此部分的实现是**重写而非直接移植**，旨在简化代码库和适应更现代的 JavaScript 风格。这可能意味着一些旧的或非主流的 JSDoc 用法可能需要调整。
*   **编辑器支持与 LSP (Language Server Protocol) 进展**:
    *   虽然大部分开发精力集中在编译器本身，但编辑器功能也在同步移植。
    *   **已实现 (早期阶段)**:
        *   错误和诊断信息的收集与显示 (Diagnostics)
        *   跳转到定义 (Go-to-definition)
        *   鼠标悬停信息 (Hover)
        *   **自动补全 (Completions)**: 这是一个新的里程碑，但围绕补全的特性如自动导入等尚未完全移植。
    *   **未来优先事项**: 移植现有的语言服务测试套件，并启用查找所有引用 (Find-all-references)、重命名 (Rename) 和签名帮助 (Signature Help)。
*   **API 进展**:
    *   目标是确保与现有 TypeScript API 消费者的兼容性。
    *   已建立一个可以通过**标准 I/O** 与 TypeScript 进程进行通信的 API 层基础。这意味着 API 消费者可以用任何语言通过 IPC 与之交互。
    *   **`libsyncrpc`**: 考虑到许多 API 消费者使用 TypeScript 和 JavaScript，并且 Node.js 本身不易实现与子进程的同步通信，微软开发了一个**用 Rust 编写的原生 Node.js 模块**，名为 `libsyncrpc`，以实现同步 API 调用。

## 已知差异、限制和注意事项

*   **功能缺失**:
    *   **`--build` 模式**: 尚不支持项目间的增量构建和项目引用，但单个项目可以使用 `tsgo` 构建。
    *   **声明文件生成 (`--declaration`)**: 当前不支持生成 `.d.ts` 文件。
    *   **降级编译**: 对旧版 JavaScript (downlevel emit targets) 的编译支持有限。
    *   **JSX Emit**: JSX 的输出目前仅限于"保留你所写的" (preserving what you wrote)，即不进行转换。
*   **配置变更**:
    *   部分在 TypeScript 6.0 中计划废弃的配置，如 `--moduleResolution node` 或 `--module commonjs`，在使用 `tsgo` 时可能会导致错误（例如 "Cannot find module" 或 "Module has no exported member"）。
    *   **建议的配置**:
        *   `"module": "preserve", "moduleResolution": "bundler"`
        *   或 `"module": "nodenext"`
    *   通常可以通过移除相关导入并依赖自动导入来解决。
*   **VS Code 扩展**: 如果遇到问题，可以通过命令 "TypeScript Native Preview: Disable" 或修改设置来临时禁用原生预览版语言服务。

## 未来展望与更新节奏

*   **目标**: 计划在 **2025 年晚些时候**发布功能更完整的编译器（包括 `--build` 支持）和大部分语言服务特性。
*   **持续更新**: TypeScript Native Previews 将会**每晚发布 (nightly builds)**，方便开发者及时获取最新的功能和修复。VS Code 扩展默认会自动更新。

微软鼓励开发者积极试用这些原生预览版，并在遇到问题或有任何建议时，通过官方渠道提交 issue 进行反馈。 