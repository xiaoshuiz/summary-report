# How to add AI Content Recommendations to your Next.js site with Vercel & OpenAI

**来源:** [Ed Spencer's Blog - AI Content Recommendations with TypeScript](https://edspencer.net/2024/9/11/ai-content-recommendations-typescript) (这篇文章是系列的核心文章)
**文章设定日期:** Sep 11, 2024 (根据文章本身发布日期)
**主要技术栈:** AI, Next.js, Vercel, OpenAI, TypeScript, React, RAG (提及概念), Embeddings

## 核心摘要

本文是一篇详细的教程，指导开发者如何在其 Next.js 网站上集成 AI 内容推荐功能。该方案利用 Vercel 进行部署，结合 OpenAI API (用于 Embeddings 和可能的 LLM 调用) 以及 TypeScript 来实现。文章重点是构建一个基于向量相似度搜索的推荐系统，为用户提供相关的其他文章或内容。

## 主要内容和看点

*   **目标**: 在 `edspencer.net` 这个 Next.js 博客网站上，根据当前文章内容，向用户推荐其他相关文章。
*   **技术选型**: 
    *   **Next.js**: 作为网站的开发框架。
    *   **Vercel**: 用于部署 Next.js 应用，并可能利用其 Serverless Functions 或 Edge Functions。
    *   **OpenAI API**: 
        *   `text-embedding-ada-002` (或更新的模型): 用于为文章内容生成向量嵌入 (Embeddings)。
        *   可能也用到了 LLM (如 GPT 系列) 来处理或生成推荐相关的文本，但主要焦点是 Embeddings。
    *   **TypeScript**: 保证类型安全和代码质量。
    *   **向量数据库/存储**: 文章暗示了需要一个地方存储所有文章的 Embeddings。虽然没有明确指定是 Pinecone 还是其他，但提到了构建时生成 Embeddings 并存储的想法。
*   **实现步骤详解**:
    1.  **内容准备与 Embedding 生成**: 
        *   在构建时 (build time)，遍历所有博客文章。
        *   对每篇文章的内容进行分块 (Chunking) 或直接使用全文（取决于文章长度和策略）。
        *   使用 OpenAI API 为每个内容块或文章生成 Embedding 向量。
        *   将这些 Embeddings 与文章元数据 (如标题、链接) 一起存储起来。这可能是一个 JSON 文件，或者一个简单的数据库，甚至是 Vercel KV 存储。
    2.  **API 路由创建 (Next.js)**:
        *   创建一个 API 路由 (e.g., `/api/recommendations`)，接收当前文章的标识 (如 slug 或 ID) 作为参数。
    3.  **实时推荐逻辑**: 
        *   当用户访问一篇文章页面时，前端调用上述 API 路由。
        *   API 路由找到当前文章的预生成 Embedding。
        *   将此 Embedding 与存储中的所有其他文章 Embeddings 进行余弦相似度 (Cosine Similarity) 计算。
        *   找出相似度最高的 N 篇文章作为推荐结果。
    4.  **前端展示 (React)**:
        *   在文章页面通过 React 组件调用推荐 API，并展示返回的推荐文章列表。
*   **讨论的优化和考量**: 
    *   **成本效益**: 在构建时生成 Embeddings 可以避免每次请求都调用 OpenAI API，从而节省成本和提高响应速度。
    *   **RAG 概念关联**: 虽然文章主要实现的是基于 Embedding 的内容相似度推荐，但作者也提到了这是构建更复杂 RAG (Retrieval-Augmented Generation) 系统的基础。推荐系统本身可以看作是一种特定形式的"检索"。
    *   **TypeScript 的作用**: 强调了 TypeScript 在定义数据结构 (如文章、Embedding、API 响应) 和保证代码健壮性方面的好处。

## 为何值得 React/TypeScript/Next.js 开发者关注

1.  **实用 AI 功能**: 内容推荐是网站和应用中非常常见且能显著提升用户参与度的功能。
2.  **现代 Web 技术栈**: 展示了如何将 AI 能力集成到基于 Next.js 和 Vercel 的现代 Web 应用中。
3.  **OpenAI API 实践**: 提供了使用 OpenAI Embeddings API 的具体代码示例和实践经验。
4.  **TypeScript 最佳实践**: 在 AI 项目中运用 TypeScript 的一个良好范例。
5.  **可扩展性**: 所描述的方法为未来扩展到更高级的 AI 功能 (如 RAG 聊天机器人) 打下了基础。

*(注：此摘要基于所提供链接中的核心文章内容分析。文章日期 "Sep 11, 2024" 是文章本身的发布日期。)* 