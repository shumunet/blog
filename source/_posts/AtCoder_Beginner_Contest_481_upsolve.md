---
title: "AtCoder Beginner Contest 481 补题"
description: "整理 AtCoder Beginner Contest 481 的赛后补题，包含题意、解题思路与代码实现。"
cover: /img/covers/acg-006.jpg
date: 2026-10-25 11:30:00
categories:
  - 算法竞赛
tags:
  - AtCoder
math: true
---

## 前言

这场其实打的挺好的，表现分居然有 $1600+$，不可思议。突然想到也好久没补题了，直接补一把！

## 			E - Most Brilliant Starry Sky 		

### 题意简述

多测，给你 $N$ 个平面直角坐标系的点，每个点都不相同，让你画一条过原点且不过任何给出点的直线，这个直线显然会把平面直角坐标系分成两部分，问点最多的那个部分包含多少个点。

### 题解

> 计算几何可恶喵 T_T

观察到一个点到原点的距离是不重要的，重要的是它从原点看出去的方向。于是就可以考虑保留每个点的**极角**。

> 极角：**极角**就是一个点相对于原点的方向角。对于点 $P(x,y)$，从原点 $O(0,0)$ 向点 $P$ 连一条射线，极角就是这条射线与 $x$ 轴正方向之间的夹角，通常规定**逆时针为正方向**。

于是我们可以把每个点变成一个圆上的点：

$$\theta_i=\arg(X_i,Y_i)$$

这也就是：

$$(\cos\theta_i,\sin\theta_i)$$

显然，到这个点一定在单位圆上。因为过原点的直线在单位圆上又会截出一条直径，设直线方向为 $\alpha$。它把平面分成两侧：

- 一侧中的方向角位于 $(\alpha,\alpha+180^\circ)$。
- 另一侧中的方向角位于 $(\alpha+180^\circ,\alpha+360^\circ)$。

把每个点映射到单位圆上，有：

- 直线与圆的两个交点是两个端点。
- 直线一侧的所有方向，正好对应圆上的一段半圆弧。
- 另一侧对应剩下的另一段半圆弧。

至此，原本的问题就变成了：

> 在圆上选一个 $180^\circ$ 的半圆，最多覆盖多少个点？

假设我们选择的直线方向是 $\alpha$，它会把平面分成两边，选择其中一边后，里面所有的点的角度都会落在：

$$ [\alpha,\alpha+\pi) $$

由于题目要求了直线一定不经过点，所以边界上是不能有点的，也就是要严格小于：

$$\theta_j-\theta_i<\pi$$

然后求出符合这个条件的最长连续区间。

这个问题显然就是排序+双指针模型了（原理是如果一个半圆覆盖了 $i$ 和 $j$ 两个点，那么它们中间的点也一定会被覆盖）。

实际实现的时候遇到了细节处理问题，圆是首尾相接的，但数组是从左到右排开的。所以如果出现：

```
350°, 355°, 2°, 8°
```

在圆上顺时针看，它们形成了一圈。要想让他们不被拆开，可以使用类似环形 DP 中常用的思想，把数组复制一遍，然后正常处理。

另外，实现时也是不需要反正切函数的，会丢精度，我们可以这样做：

极角排序可以用：

- 上半平面判断。
- 叉积比较两个向量的先后。

窗口是否合法也可以用叉积判断：

对于排序后的两个向量 $\vec a,\vec b$：

$$ \vec a\times\vec b>0 $$

表示从 $\vec a$ 逆时针转到 $\vec b$ 的角度小于 $180^\circ$。

（实际上这部分我还没有学会，如果有懂的师傅欢迎交流 T_T）

```c++
#include<bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'
#define int long long

struct Point {
    int x,y;
};

int cross(Point a,Point b) {
    return a.x*b.y-a.y*b.x;
}

bool upper(Point p) {
    return p.y>0||(p.y==0&&p.x>0);
}

bool cmp(Point a,Point b) {
    bool ua=upper(a);
    bool ub=upper(b);
    if(ua!=ub) {
        return ua>ub;
    }
    return cross(a,b)>0;
}

void solve() {
    int n;
    cin>>n;
    vector<Point> a(n);
    for(int i=0;i<n;i++) {
        cin>>a[i].x>>a[i].y;
    }
    sort(a.begin(),a.end(),cmp);
    vector<Point> b=a;
    for(auto p:a) b.push_back(p);
    int ans=1,r=0;
    for(int l=0;l<n;l++) {
        if(r<l+1) r=l+1;
        while(r<l+n&&cross(b[l],b[r])>0) r++;
        ans=max(ans,r-l);
    }
    cout<<ans<<endl;
}

signed main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T = 1;
    cin>>T;
    while (T--) {
        solve();
    }
    return 0;
}

```

