---
title: "AVL学习笔记"
description: "介绍 AVL 树的平衡因子、四种旋转情况及插入、删除操作，并实现普通平衡树。"
cover: /img/covers/anime-01.webp
date: 2026-10-17 11:00:00
categories:
  - 算法竞赛
tags:
  - 学习笔记
  - 数据结构
math: true

---

## 前言

在普通的二叉搜索树中，如果我们要构建的序列本身是有序的，那么就会变成链式结构，退化为 $O(n)$。

```
10
  \
   20
     \
      30
```

为了应对这个问题，平衡二叉树出现了。所谓的平衡二叉树，就是能让一棵树在失衡的时候能够通过某些操作重新平衡的二叉搜索树。

本文将对 AVL 树进行初步的认识和代码的实现。

## 相关概念

### 平衡因子

对一个结点来说，定义它的左子树高度减右子树高度为平衡因子。

### 失衡

当一个结点的平衡因子绝对值大于 1，则该结点失衡。

### 左旋

左旋操作就是把一个结点向左旋转，同时把冲突的左孩子变成右孩子。看上去不太容易懂，我们这里以下面的二叉搜索树为例：

```
  x
   \
    y
   / \
  B   C
```

左旋后：

```
    y
   / \
  x   C
   \
    B
```

这里的大小关系可以自行根据二叉搜索树的定义来推导，不再赘述。

通过对两棵二叉搜索树进行中序遍历，我们发现是相同的，所以这两棵二叉搜索树是等价的。

### 右旋

右旋操作就是把一个结点向右旋转，同时把冲突的右孩子变成左孩子。看上去不太容易懂，我们这里以下面的二叉搜索树为例：

```
      y
     /
    x
   / \
  A   B
```

右旋后：

```
    x
   / \
  A   y
     /
    B
```

这里的大小关系可以自行根据二叉搜索树的定义来推导，不再赘述。

通过对两棵二叉搜索树进行中序遍历，我们发现是相同的，所以这两棵二叉搜索树是等价的。

## 插入结点

我们发现插入结点后，如果这棵树有结点失衡，则可以分成下面的四种情况：

### LL 型：右旋

对于我们新插入的结点是左子树的左结点导致这棵树有结点失衡，则称为 LL 型。

```
    30
   /
  20
 /
10
```

对于 LL 型造成的失衡，我们只需要进行一次右旋即可解决失衡的问题。

```
   20
  /  \
10   30
```

### RR 型：左旋

对于我们新插入的结点是右子树的右结点导致这棵树有结点失衡，则称为 RR 型。

```
10
  \
   20
     \
      30
```

对于 RR 型造成的失衡，我们只需要进行一次左旋即可解决失衡的问题。

```
   20
  /  \
10   30
```

### LR 型：左旋左再右

对于我们新插入的结点是左子树的右结点导致这棵树有结点失衡，则称为 LR 型。

```
   30
  /
10
  \
   20
```

我们可以通过先左旋左子树再右旋的方式解决失衡的问题。对于上面这棵二叉搜索树，我们就可以先左旋 10。

```
   30
  /
 20
 /
10
```

然后再右旋 30，问题就解决了。

```
   20
  /  \
10   30
```

### RL型： 右旋右再左

对于我们新插入的结点是右子树的左结点导致这棵树有结点失衡，则称为 RL 型。

```
10
  \
   30
  /
20
```

类似的两次操作：

```
10
  \
   20
     \
      30
```

```
   20
  /  \
10   30
```

### 多个结点失衡

有时候，我们插入一个结点后会导致多个结点失衡，这时有一个性质：

> 插入结点后导致多个祖先结点失衡，只需要调整**距离插入结点最近的失衡结点**，其他的失衡结点会自动平衡。

至于证明就不谈了，但是这启发了我们处理插入结点问题的基本步骤：

1. 按照 BST 规则插入，得到二叉搜索树。
2. 从插入结点向上检查平衡因子。
3. 找到第一个失衡结点，根据路径判断属于哪种类型，作出对应的操作。
4. 更新高度。

## 更简单的判定方式

如果记录路径的话，还是有些复杂，这里提供一种更简单的判定失衡类型的方式：

| $BF(z)$ | 子结点平衡因子 | 类型 | 操作     |
| ------- | -------------- | ---- | -------- |
| $+2$    | $\ge 0$        | LL   | 右旋     |
| $+2$    | $<0$           | LR   | 先左后右 |
| $-2$    | $\le 0$        | RR   | 左旋     |
| $-2$    | $>0$           | RL   | 先右后左 |

其中，约定 $BF(z)$ 为 $z$ 的平衡因子。

也就是说，**某个结点的平衡因子为 $+2$ 时，则说明是 L某 型，通过看左结点的平衡因子决定类型；某个结点的平衡因子为 $-2$ 时，则说明是 R某 型，通过看右结点的平衡因子决定类型。**

## 删除结点

删除结点的操作其实与插入结点的操作大体相似，不同的是**删除时调整失衡祖先后需要继续向上调整**。

所以分为以下两步：

1. 按照 BST 规则删除
   - 没有孩子：直接删除。
   - 一个孩子：用孩子替代。
   - 两个孩子：用中序后继或前驱替代。
2. 从删除位置向上回溯

## P3369 【模板】普通平衡树

### 题意简述

需要动态地维护一个可重集合 $M$，并且提供以下操作：

1. 向 $M$ 中插入一个数 $x$。
2. 从 $M$ 中删除一个数 $x$。（若有多个相同的数，应只删除一个）
3. 查询 $M$ 中有多少个数比 $x$ 小，并且将得到的答案加 $1$。
4. 查询如果将 $M$ 从小到大排列后，排名位于第 $x$ 位的数。
5. 查询 $M$ 中 $x$ 的前驱（定义为 $M$ 中小于 $x$，且最大的数）。
6. 查询 $M$ 中 $x$ 的后继（定义为 $M$ 中大于 $x$，且最小的数）。

对于操作 $3,5,6$，**不保证**当前可重集中存在数 $x$。 对于操作 $4,5,6$，保证答案一定存在。

### 题解

对于这道题，因为是可重的，所以我们必须对每个结点维护出现的次数 `cnt` 才能进行删除操作。

因为要平衡，所以我们必然要维护子树高度。

因为要维护前驱后继和比某个数小的元素个数，所以肯定要维护结点的子树的元素个数。

```c++
struct Node {
    int key;       // 结点值
    int cnt;       // key 出现次数
    int size;      // 子树中元素总数
    int height;    // 子树高度
    Node *left;    // 左孩子
    Node *right;   // 右孩子

    Node(int value) {
        key = value;
        cnt = 1;
        size = 1;
        height = 1;
        left = nullptr;
        right = nullptr;
    }
};
```

接下来是一些获取信息的函数，都是比较简单的，这里主要是判定是否存在。

```c++
int getHeight(Node *root) {
    if(root == nullptr) {
        return 0;
    }
    return root->height;
}

int getSize(Node *root) {
    if(root == nullptr) {
        return 0;
    }
    return root->size;
}
```

接下来就是更新结点信息的函数了，这个也比较简单，根据代码就能理解了。

```c++
void pushUp(Node *root) {
    if(root == nullptr) return;
    int leftHeight = getHeight(root->left);
    int rightHeight = getHeight(root->right);
    root->height = max(leftHeight,rightHeight) + 1;
    root->size = getSize(root->left) + getSize(root->right) + root->cnt;
}
```

获取平衡因子的函数也很简单，用我们刚刚写好的获取信息就行了。

```c++
int getBalance(Node *root) {
    if(root == nullptr) {
        return 0;
    }
    return getHeight(root->left) - getHeight(root->right);
}
```

接下来是关键的旋转函数：

```c++
Node *rotateLeft(Node *x) {
    Node *y = x->right;
    Node *mid = y->left;
    y->left = x;
    x->right = mid;
    pushUp(x);
    pushUp(y);
    return y;
}

Node *rotateRight(Node *x) {
    Node *y = x->left;
    Node *mid = y->right;
    y->right = x;
    x->left = mid;
    pushUp(x);
    pushUp(y);
    return y;
}
```

这两个函数需要返回值的原因是：**旋转不仅要修改子树内部的指针，还要让外面知道：这棵子树的根换了。**

这使得我们后面需要把新的子树根交给调用者，调用时需要类似于：

```c++
root = rotateLeft(root);
```

维持平衡性的函数：

```c++
Node *maintain(Node *root) {
    if(root == nullptr) {
        return nullptr;
    }
    pushUp(root); //不能忘记！！！
    int balance = getBalance(root);
    if(balance > 1) { //左子树高，是L某型
        if(getBalance(root->left) < 0) { //LR
            root->left = rotateLeft(root->left);
        }
        return rotateRight(root);
    }
    if(balance < -1) { //右子树高，是R某型
        if(getBalance(root->right) > 0) { //RL
            root->right = rotateRight(root->right);
        }
        return rotateLeft(root);
    }
    return root;
}
```

插入函数：

```c++
Node *insert(Node *root, int value) {
    if (root == nullptr) {
        return new Node(value);
    }

    if (value == root->key) {
        root->cnt++;
        pushUp(root);
        return root;
    }

    if (value < root->key) {
        // 插入后，左子树的根可能改变，必须重新连接
        root->left = insert(root->left, value);
    } else {
        root->right = insert(root->right, value);
    }

    return maintain(root);
}
```

接下来是最复杂的部分：删除操作。

我们先写删除整个结点的部分，因为后继结点的 `key` 和 `cnt` 会整体复制，所以后继结点必须整个删除。

比如说我们想删除 20：

```
       20（1 次）
      /  \
    10   30（3 次）
```

因为 20 有两个孩子，所以会找到它的后继 30，然后复制：

```c++
root->key = successor->key;
root->cnt = successor->cnt;
```

得到了：

```
       30（3 次）
      /  \
    10   30（3 次）
         ↑ 原来的后继结点
```

这就需要我们删除原来的后继结点：

```
root->right = eraseAll(root->right, successor->key);
```

得到：

```
       30（3 次）
      /
    10
```

代码如下：

```c++
Node *getMin(Node *root) {
    while(root->left != nullptr) root=root->left;
    return root;
}

Node *eraseAll(Node *root,int value) {
    if(root == nullptr) return nullptr;
    if(value < root->key) {
        root->left=eraseAll(root->left,value);
    }
    else if(value > root->key){
        root->right=eraseAll(root->right,value);
    }
    else {
        //就一个孩子
        if(root->left == nullptr || root->right ==nullptr) {
            Node *child = nullptr;
            if(root->left != nullptr) {
                child = root->left;
            }
            else {
                child = root->right;
            }
            delete root;
            return child;    
        }
        //此时有两个孩子，就不能直接返回一个孩子连上去了，我们需要给他俩处理好顺序再返回
        //先完整复制再删除
        Node *successor = getMin(root->right);
        root->key = successor->key;
        root->cnt = successor->cnt;
        root->right = eraseAll(root->right,successor->key);
    }
    return maintain(root);
}
```

删除一个数就简单了，可以复用这里的删除整个结点：

```c++
Node *eraseOne(Node *root,int value) {
    if(root == nullptr) return nullptr;
    if(value < root->key) {
        root->left = eraseOne(root->left,value);
    }
    else if(value > root->key) {
        root->right = eraseOne(root->right,value);
    }
    else {
        //有多个相同的就只删除一个
        if(root->cnt > 1) {
            root->cnt--;
            pushUp(root);
            return root;
        }
        //否则就要删除整个结点
        else {
            return eraseAll(root,value);
        }
    }
    return maintain(root);
}
```

至此，一棵平衡树就写完了，接下来就是一些维护信息的内容了，这部分比较简单且每个题目不一样，我就一笔带过了。

```c++
int getRank(Node *root,int value) {
    if(root == nullptr) return 1;
    if(value == root->key) {
        return getSize(root->left) + 1;
    }
    if(value < root->key) {
        return getRank(root->left,value);
    }
    return getSize(root->left) + root->cnt + getRank(root->right,value);
}

int getKth(Node *root,int rank) {
    if(root == nullptr) return 0;
    int leftSize = getSize(root->left);
    if(rank <= leftSize) {
        return getKth(root->left,rank);
    }
    if(rank <= leftSize +root->cnt) {
        return root->key;
    }
    int newRank = rank - leftSize - root->cnt;
    return getKth(root->right,newRank);
}

int getPredecessor(Node *root, int value) {
    int answer = 0;
    while (root != nullptr) {
        if (root->key < value) {
            answer = root->key;
            root = root->right;
        } else {
            root = root->left;
        }
    }
    return answer;
}

int getSuccessor(Node *root, int value) {
    int answer = 0;
    while (root != nullptr) {
        if (root->key > value) {
            answer = root->key;
            root = root->left;
        } else {
            root = root->right;
        }
    }
    return answer;
}
```

这里主要是你要分清楚答案是在哪棵子树，然后去递归处理就行，但是需要进行大量的分类讨论。

至此，我们这道题的所有需要维护的操作都写完了，我们可以舒适地写个主函数然后享受 AC 了！

```c++
#include<bits/stdc++.h>
using namespace std;
struct Node {
    int key;       // 结点值
    int cnt;       // key 出现次数
    int size;      // 子树中元素总数
    int height;    // 子树高度
    Node *left;    // 左孩子
    Node *right;   // 右孩子

    Node(int value) {
        key = value;
        cnt = 1;
        size = 1;
        height = 1;
        left = nullptr;
        right = nullptr;
    }
};

int getHeight(Node *root) {
    if(root == nullptr) {
        return 0;
    }
    return root->height;
}

int getSize(Node *root) {
    if(root == nullptr) {
        return 0;
    }
    return root->size;
}

void pushUp(Node *root) {
    if(root == nullptr) return;
    int leftHeight = getHeight(root->left);
    int rightHeight = getHeight(root->right);
    root->height = max(leftHeight,rightHeight) + 1;
    root->size = getSize(root->left) + getSize(root->right) + root->cnt;
}

int getBalance(Node *root) {
    if(root == nullptr) {
        return 0;
    }
    return getHeight(root->left) - getHeight(root->right);
}

Node *rotateLeft(Node *x) {
    Node *y = x->right;
    Node *mid = y->left;
    y->left = x;
    x->right = mid;
    pushUp(x);
    pushUp(y);
    return y;
}

Node *rotateRight(Node *x) {
    Node *y = x->left;
    Node *mid = y->right;
    y->right = x;
    x->left = mid;
    pushUp(x);
    pushUp(y);
    return y;
}

Node *maintain(Node *root) {
    if(root == nullptr) {
        return nullptr;
    }
    pushUp(root); //不能忘记！！！
    int balance = getBalance(root);
    if(balance > 1) { //左子树高，是L某型
        if(getBalance(root->left) < 0) { //LR
            root->left = rotateLeft(root->left);
        }
        return rotateRight(root);
    }
    if(balance < -1) { //右子树高，是R某型
        if(getBalance(root->right) > 0) { //RL
            root->right = rotateRight(root->right);
        }
        return rotateLeft(root);
    }
    return root;
}

Node *insert(Node *root,int value) {
    if(root == nullptr) return new Node(value);
    if(value == root->key) {
        root->cnt++;
        pushUp(root);
        return root;
    }
    if(value < root->key) {
        root->left = insert(root->left, value);
    }
    else {
        root->right = insert(root->right, value);
    }
    return maintain(root);
}

Node *getMin(Node *root) {
    while(root->left != nullptr) root=root->left;
    return root;
}

Node *eraseAll(Node *root,int value) {
    if(root == nullptr) return nullptr;
    if(value < root->key) {
        root->left=eraseAll(root->left,value);
    }
    else if(value > root->key){
        root->right=eraseAll(root->right,value);
    }
    else {
        //就一个孩子
        if(root->left == nullptr || root->right ==nullptr) {
            Node *child = nullptr;
            if(root->left != nullptr) {
                child = root->left;
            }
            else {
                child = root->right;
            }
            delete root;
            return child;    
        }
        //此时有两个孩子，就不能直接返回一个孩子连上去了，我们需要给他俩处理好顺序再返回
        //先完整复制再删除
        Node *successor = getMin(root->right);
        root->key = successor->key;
        root->cnt = successor->cnt;
        root->right = eraseAll(root->right,successor->key);
    }
    return maintain(root);
}

Node *eraseOne(Node *root,int value) {
    if(root == nullptr) return nullptr;
    if(value < root->key) {
        root->left = eraseOne(root->left,value);
    }
    else if(value > root->key) {
        root->right = eraseOne(root->right,value);
    }
    else {
        //有多个相同的就只删除一个
        if(root->cnt > 1) {
            root->cnt--;
            pushUp(root);
            return root;
        }
        //否则就要删除整个结点
        else {
            return eraseAll(root,value);
        }
    }
    return maintain(root);
}

int getRank(Node *root,int value) {
    if(root == nullptr) return 1;
    if(value == root->key) {
        return getSize(root->left) + 1;
    }
    if(value < root->key) {
        return getRank(root->left,value);
    }
    return getSize(root->left) + root->cnt + getRank(root->right,value);
}

int getKth(Node *root,int rank) {
    if(root == nullptr) return 0;
    int leftSize = getSize(root->left);
    if(rank <= leftSize) {
        return getKth(root->left,rank);
    }
    if(rank <= leftSize +root->cnt) {
        return root->key;
    }
    int newRank = rank - leftSize - root->cnt;
    return getKth(root->right,newRank);
}

int getPredecessor(Node *root, int value) {
    int answer = 0;
    while (root != nullptr) {
        if (root->key < value) {
            answer = root->key;
            root = root->right;
        } else {
            root = root->left;
        }
    }
    return answer;
}

int getSuccessor(Node *root, int value) {
    int answer = 0;
    while (root != nullptr) {
        if (root->key > value) {
            answer = root->key;
            root = root->left;
        } else {
            root = root->right;
        }
    }
    return answer;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    Node *root = nullptr;
    while (n--) {
        int opt, x;
        cin >> opt >> x;
        if (opt == 1) {
            root = insert(root, x);
        } else if (opt == 2) {
            root = eraseOne(root, x);
        } else if (opt == 3) {
            cout << getRank(root, x) << '\n';
        } else if (opt == 4) {
            cout << getKth(root, x) << '\n';
        } else if (opt == 5) {
            cout << getPredecessor(root, x) << '\n';
        } else if (opt == 6) {
            cout << getSuccessor(root, x) << '\n';
        }
    }
    return 0;
}
```

