---
title: "Codeforces Round 1123 (Div. 2) 游记"
description: "整理 Codeforces Round 1123 的 A 至 D 题，包含题意、解题思路与代码实现。"
cover: /img/covers/anime-03.webp
date: 2026-09-26 01:00:00
categories:
  - 算法竞赛
tags:
  - Codeforces
math: true
---

## 赛时状况

这场应该是我个人打的比较满意的一场，因为这是我历史上第二次赛时切出了 Div2 的 D 题，开心喵～

## A. Turn Into a Palindrome

### 题意简述

有一个字符串和一个字符，每次操作就是选择字符串中的某一位把它变为这个字符，问最小的把这个字符串变为回文字符串的操作次数。

### 题解

容易观察到对于一个长度为 $n$ 的回文字符串 $S$ ，必须所有的 $S_i$ 都等于 $S_(n-i-1)$ 才行，那么我们从头扫描到 $\frac{n}{2}$ ，如果这一位和它的对应位相等那么我们不需要有任何的花费，否则就要花费，那花费多少呢？容易想到要么操作 $1$ 次要么操作 $2$ 次，那就很简单了，如果这一位或者它的对应位有一个是可以操作得到的字符就花费 $1$ 把它另一半操作掉，否则就必须同时操作掉，花费是 $2$，这样就写完了。

```c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n;
    char c;
    string s;
    cin>>n>>c;
    cin>>s;
    int ans=0;
    for(int i=0;i<n/2;i++) {
        int j=n-i-1;
        if(s[i]==s[j]) continue;
        if(s[i]==c||s[j]==c) ans++;
        else ans+=2;
    }
    cout<<ans<<endl;
}

int main() {
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

## B. Fashionable Array

### 题意简述

给定一个长度为 $n$ 的整数数组，可以任意重新排列数组中的元素。

对于每个前缀，定义其“众数”为出现次数最多的数字；如果有多个数字出现次数相同，则取数值最大的那个。

要求构造一个重新排列后的数组，使得所有前缀的众数之和最大，并输出这个排列后的数组。

### 题解

读完题就感觉是贪心题，最大的数肯定得让它放在最前面，然后接下来让次大的数放跟最大的数这么多个就行了，能放完最好，放不完就留下来等所有的数都放过了之后再放，不然众数会变小，这样绝对是不劣的，然后想想怎么写代码就行了，值得一提的是，我之前不知道可以用 `map<int,int,greater<int>> mp;` 这种东西来让 $map$ 从大到小排序，但是我赛时发明出来了，哈哈。

```c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define int long long
#define endl '\n'

void solve() {
    int n;
    map<int,int,greater<int>> mp;
    cin>>n;
    vector<int>a(n+1,0);
    for(int i=1;i<=n;i++) {
        cin>>a[i];
        mp[a[i]]++;
    }
    int cnt=0;
    int ans=0;
    while(cnt<n) {
        int mx=mp.begin()->first;
        for(auto it=mp.begin();it!=mp.end();) {
            ans+=mx;
            cnt++;
            cout<<it->first<<" ";
            it->second--;
            if(it->second==0) {
                it=mp.erase(it);
            }
            else {
                it++;
            }
        }
    }
    cout<<endl;
    //cout<<ans<<endl;
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

## C. GCD Treasury

### 题意简述

有 $n$ 堆硬币，第 $i$ 堆有 $a_i$ 个，初始有一个数 $x$。

每次可以选择一堆满足：

$$ a_i>0,\qquad \gcd(a_i,x)>1 $$

的硬币，令：

$$ g=\gcd(a_i,x) $$

然后拿走这堆中的 $g$ 个硬币，并把 $x$ 修改为 $g$。

当不存在可选的堆时结束。

要求合理安排选择顺序，求出最大的拿走的硬币总数。

### 题解

一开始还以为是神秘数论题，但是读着读着感觉像图论或者动态规划，然后手玩了几把样例，好像就有点思路了。

每次操作都会把 $x$ 变成它和某个 $a_i$ 的 gcd，所以不管怎么选，$x$ 肯定一直是初始值的约数，那就可以拿这些约数当状态做 DP 了。

然后考虑当前 $x=p$，如果有一堆硬币数是 $p$ 的倍数，那每次都能拿走 $p$ 个，而且 $x$ 不变，直接把这一堆拿空就行了。反正拿完也不影响后面的选择，所以所有 $p$ 的倍数都可以先拿完。记这些堆的硬币总数为 $sum[p]$。

设 $dp[p]$ 表示当前 $x=p$，并且已经拿完所有 $p$ 的倍数时，最多拿了多少硬币。接下来枚举一堆还没拿过的硬币，令 $q=\gcd(a_i,p)$，如果 $1<q<p$，就可以把状态变成 $q$。这时候所有 $q$ 的倍数也都能拿完了，不过之前已经拿过的不能重复算，所以新增的硬币数就是 $sum[q]-sum[p]$，转移就是：

$$ dp[q]=\max(dp[q],dp[p]+sum[q]-sum[p]). $$

值得注意的是，之前拿过的堆都是 $p$ 的倍数，而这次选的堆满足 $\gcd(a_i,p)<p$，所以它肯定还没被拿过。

尽管思路比较简单，但是实现起来还挺复杂的，累死俺了喵。

```c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'
#define int long long

bool cmp(int a,int b) {
    return a>b;
}
int gcd(int a,int b) {
    if(b==0) return a;
    return gcd(b,a%b);
}
void solve() {
    int n,x;
    cin>>n>>x;
    vector<int>a(n+1,0);
    for(int i=1;i<=n;i++) {
        cin>>a[i];
    }
    if(x==1) {
        cout<<0<<endl;
        return;
    }
    vector<int>divs;
    for(int i=1;i*i<=x;i++) {
        if(x%i==0) {
            divs.push_back(i);
            if(i*i!=x) divs.push_back(x/i);
        }
    }
    sort(divs.begin(),divs.end(),cmp);
    int m=divs.size();
    map<int,int> ht;
    for(int i=0;i<m;i++) {
        ht[divs[i]]=i;
    }
    vector<int>v(m,0);
    vector<int>cnt(m,0);
    for(int tmp:a) {
        int g=gcd(tmp,x);
        int k=ht[g];
        v[k]+=tmp;
        cnt[k]++;
    }
    vector<int> ps;
    vector<int> sum(m,0);
    for(int i=0;i<m;i++) {
        if(cnt[i]>0) ps.push_back(i);
    }
    for(int i=0;i<m;i++) {
        for(int j:ps) {
            if(divs[j]%divs[i]==0) {
                sum[i]+=v[j];
            }
        }
    }
    vector<int> dp(m,-INF);
    int st=ht[x];
    dp[st]=sum[st];
    for(int i=0;i<m;i++) {
        if(dp[i]==-INF) continue;
        int p=divs[i];
        for(int j:ps) {
            int tmp=gcd(p,divs[j]);
            if(tmp>1&&tmp<p) {
                int k=ht[tmp];
                dp[k]=max(dp[k],dp[i]+sum[k]-sum[i]);
            }
        }
    }
    int ans=0;
    for(int i:dp) {
        ans=max(ans,i);
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

## D. Backrooms Hill

### 题意简述

给定一个长度为 $n$ 的排列。

每次可以交换两个**中间隔着一个数**的元素，例如交换第 $1$ 个和第 $3$ 个元素。操作次数不限。

问能否把排列变成**先严格递增、再严格递减**的“山形”。完全递增或完全递减也算。

能做到输出 `YES`，否则输出 `NO`。

### 题解

手玩了一下样例，然后注意到了这道题跟某个数字所在位置的奇偶性应该是很有关系的，再根据数据范围推测出应该是要观察结论的。

注意到如果长度是奇数，并且 $1$ 在偶数位置，那就一定无解，为什么呢？

首先说一个结论：**最小数一定是放在端点的**

原因是如果不放在端点的话就无法满足单调性了，会形成一个”山谷“，不符合题意。

而每次可以交换两个**中间隔着一个数**的元素，如果 $1$ 在偶数位置的话它只能换去别的偶数位置，但是如果长度是奇数的话它没法放在第一个位置或者最后一个位置，所以就错了。

我们考虑推广，如果把一个数 $x$ 放在了奇数位置，它会导致 $x+1$ 只能放在偶数位置，反之也同理，那么就意味着相邻的两个数的位置的奇偶性一定是不同的，这样的话就做完了，至于怎么证明我就不会了（doge）。

``` c++
#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const int MOD = 1e9 + 7;
const ll INF = 4e18;
const int MAXN = 2e5+100;
#define endl '\n'

void solve() {
    int n;
    cin>>n;
    vector<int>pos(n+1,0);
    for(int i=1;i<=n;i++) {
        int x;
        cin>>x;
        pos[x]=i&1;
    }
    bool flag=true;
    if((pos[1]==0)&&(n&1)) {
        flag=false;
    }
    for (int i=n;i>=2;i-= 2) {
        if(pos[i]==pos[i-1]) {
            flag=false;
        }
    }
    if(flag) cout<<"YES"<<endl;
    else cout<<"NO"<<endl;
}

int main() {
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
