> 引用：
>
> - LeetCode热题100（100道题17个主题）：https://leetcode.cn/studyplan/top-100-liked/
>- 剑指offer（50道题）：https://leetcode.cn/problem-list/XApvNy3p/



# LeetCode热题100

解题语言使用python3。目录：

- 第一章 哈希
- 第二章 双指针
- 第三章 滑动窗口
- 第四章 子串
- 第五章 普通数组
- 第六章 矩阵
- 第七章 链表
- 第八章 二叉树
- 第九章 图论
- 第十章 回溯
- 第十一章 二分查找
- 第十二章 栈
- 第十三章 堆
- 第十四章 贪心算法
- 第十五章 动态规划
- 第十六章 多维动态规划
- 第十七章 技巧



## 第一章 哈希

### 1题，#哈希表，两数之和

#### 题目

题目要求找出数组中的两个数，这两个数的和为指定值。

#### 解法 

思路有以下3点：

- 将数组的所有元素放进哈希表中；
- 用 sum-num[i] = target，判断target是否在哈希表中；
- 如果存在，找出其下标不为自身，即得答案，否则继续遍历。

#### 代码

```python
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        nset = set()
        for num in nums:
            nset.add(num)
        for i, num in enumerate(nums):
            if target-num not in nset:
                continue
            for j, peer in enumerate(nums):
                if i!=j and peer==target-num:
                    return [i, j]
        return []
```

### 49题，#哈希表，字母异位词分组

#### 题目

给你一个列表，对列表中的元素按照字母异位词进行分组。

输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

输出: [["bat"],["nat","tan"],["ate","eat","tea"]]

#### 解法

给字母组合一个规则，让一组字母异位词拥有同一个模板。

- 模版：将字母组合按字母表排序；
- 空间：使用字典将相同模版的异位词归拢到一起。

#### 代码

```python
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        map = {}
        for s in strs:
            ss = ''.join(sorted(s))
            map.setdefault(ss, []).append(s)
        # return list(map.values()) # 击败55%
        return [map[key] for key in map] # 击败93% 为什么更好
```

### 128题，#哈希表，#并查集，最长连续序列

#### 题目

给你一个未排序数组，找出数字连续的最长序列。

输入：nums = [100,4,200,1,3,2]

输出：4

解释：最长数字连续序列是 [1, 2, 3, 4]。它的长度为 4。

#### 解法

- 空间：将数组放进哈希表里面，方便找数；
- 外层遍历：遍历数组中的连续序列起点num，也就是num-1不在哈希表中
- 内层遍历：遍历num+1 in 哈希表，维护一个全局最长序列长度值

#### 代码

```python
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        nums_set = set(nums)
        mx_len = 1
        for num in nums_set:
            if num - 1 not in nums_set:
                cur_len = 1
                while(num + 1 in nums_set):
                    cur_len += 1
                    num += 1
                mx_len = max(mx_len, cur_len)
        return mx_len
```

## 第二章 双指针

### 283题，#数组，#双指针，移动零

#### 题目

给你一个数组，将数组中的零移动到末尾，要求原地操作。

#### 解法

使用双指针。

- 左指针：当前不含零的前缀序列；
- 右指针：当前遍历的下标。

#### 代码

```python
class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        left, right = -1, -1
        for i, num in enumerate(nums):
            if num == 0:
                if left == -1:
                    left = right = i
                else:
                    right += 1
            else:
                if left != -1:
                    nums[left] = num
                    nums[i] = 0
                    left += 1
                    right += 1
```

### 11题，#数组，#双指针，盛最多水的容器

#### 题目

找到两根柱子，能够兜住最多的水。

![11题描述](./assets/question_11-9097013-9097018.jpg)

图1-11题描述

#### 解法

使用双指针，从两边往中间移动。

- 记录一个全局最大值；
- 左指针和右指针的高度，谁小谁就往中间移动，直到两指针相遇。

这里解释一下移动的原理，如果左边高度>右边高度，那么，

- 不管左指针往中间移多少步，容量都不可能更大了；
- 不管左指针往右边移多少步，如果存在更大值，都已经被记录过了，不要忘了，双指针是从两端开始遍历的，局部最优值会在全局最大值上更新。

左边高度<右边高度同理；如果高度相等，移动左边或者右边都行。

#### 代码

```python
class Solution:
    def maxArea(self, height: List[int]) -> int:
        l, r = 0, len(height)-1
        mx = 0
        while(l < r):
            mx = max(mx, min(height[l], height[r])*(r-l))
            if height[l] <= height[r]:
                l += 1
            else:
                r -= 1
        return mx
```

### <span style="color:red;">15题，#数组，#双指针，三数之和（看不懂解析）</span>

#### 题目

给你一个数组，找出所有三元组，下标不同，同时和为0。注意三元组不要重复。

### 42题，#数组，#动态规划，接雨水

#### 题目

这样一堆柱子，下雨后能够接住多少雨水。

![42题目描述](./assets/rainwatertrap.png)

图2-42题描述

#### 解法

- 先从左往右遍历：让每个水柱尽可能高

- 再从右往左遍历：将兜不住的部分抹掉

#### 代码

```python
class Solution:
    def trap(self, height: List[int]) -> int:
        if len(height) < 3:
            return 0

        space = [height[0]]
        mx = height[0]
        res = 0
        for i in range(1, len(height)):
            if height[i] > mx:
                mx = height[i]
            space.append(mx)

        space[-1] = mx = height[-1]
        for i in range(len(height)-2, -1, -1):
            if height[i] > mx:
                mx = height[i]
            if space[i] > mx:
                space[i] = mx
            res += (space[i]-height[i])
        return res
```

## 第三章 滑动窗口

### 3题，#字符串，#哈希表，#滑动窗口，无重复字符的最长子串

#### 题目

给定一个字符串，找出不含重复字母的最长子串的长度

#### 解法

- 滑动窗口，起始位置在头部，遍历字符串，滑动窗口维护当前局部最长子串
- 哈希表，保存滑动窗口中间已经出现过的字母。

#### 代码

```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        sdict = {}
        mx = 0
        l = 0
        for r in range(len(s)):
            if s[r] not in sdict:
                sdict[s[r]] = r
                mx = max(mx, r-l+1)
                continue
            newl = sdict[s[r]]+1
            sdict[s[r]] = r
            for i in range(l, newl-1):
                del sdict[s[i]]
            l = newl
        return mx
```

### 438题，#字符串，#哈希表，#滑动窗口，找到字符串中所有字母异位词

#### 题目

给定字符串s和p，找出s中以p为模版的异位词的起始索引。不需要考虑输出顺序。

#### 思路

- 计数板：记录窗口中各个字母个数和模版串中的差异。比如：缺失2个'a'、多出来3个'b' 记为 {'a': -2, 'b': 3}
- differ: int，这个值用来记录窗口中一共有多少类字母和模版存在差异。比如计数板为 {'a': -2, 'b': 3，'c': 0}，那么differ就等于2，因为只有'a'和'b'这2类字母个数和模版存在差异。
- 移动窗口：使用for循环移动窗口，更新计数板。同时检查下面2件事：
    - 本次移出窗口的字母，是否刚好消除了一类字母差异；
    - 本次新加入窗口的字母，是否刚好消除了一类字母的差异；

- 在循环中，最后检查是否消除了所有类字母的差异，如果是，那么就是找出了一种期望情况。

最后，这道题目初次接触还是蛮难的，同时也是滑动窗口类型中非常经典的一道题。

#### 代码

```python
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:

        # 记录滑动窗口中每个字母个数和p的差异
        # 值为正：该字母s比p多n个
        # 值为负：该字母s比p少n个
        # 值为0：该字母s和p一样多
        count = [0] * 26  
        s_len = len(s)
        p_len = len(p)

        if s_len < p_len:
            return []
            
        res = []  # 保存结果

        for i in range(p_len):
            count[ord(s[i]) - 97] += 1
            count[ord(p[i]) - 97] -= 1
        
        # 记录现在有多少个字母个数不同
        differ = [ c!=0 for c in count].count(True)

        if differ == 0:
            res.append(0)
        
        # 从第0个开始去除，直到去掉第s_len-p_len个
        for i in range(s_len - p_len):
            # differ只需要判断临界情况
            if count[ord(s[i])-97] == 1:
                differ -= 1
            elif count[ord(s[i])-97] == 0:
                differ += 1
            count[ord(s[i])-97] -= 1

            if count[ord(s[i+p_len])-97] == -1:
                differ -= 1
            elif count[ord(s[i+p_len])-97] == 0:
                differ += 1
            count[ord(s[i+p_len])-97] += 1

            if differ == 0:
                res.append(i+1)

        return res
```

## 第四章 子串

### 560题，#数组，#哈希表，#前缀和，和为k的子数组

#### 题目

给定一个数组和数字，找出所有和为k的子数组，你最终只需要统计这样的数组有多少个。ps：子数组是数组中元素的连续非空序列。

#### 思路

- 前缀和与哈希表：遍历一次，我们能得到所有从[0～i]元素的和，那么将这些前缀和存进哈希表中
- 在for循环中，前缀和的列表为[1，3，3，8, 12]，目标和为9，那么12-9=3，我们到哈希表{1:1, 3:2, 8:1, 12:1}中找到前缀和为3的索引有2个，那么就等于找到了2种期望的情况

最终总共遍历一次就可以得到最终答案了，还有一点需要指出的是，我们并不需要保存前缀和的列表，只需要前缀和的哈希表即可，具体可以根据代码理解一下。

#### 代码

```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        pre, res = 0, 0
        pcount = {0: 1}

        for x in nums:
            pre += x
            if pre - k in pcount:
                res += pcount[pre - k]

            pcount[pre] = pcount.setdefault(pre, 0) + 1
            
        return res
```



### 239题，#子串，#数组，#滑动窗口，滑动窗口的最大值

#### 题目

给定一个数组，和一个大小为k的滑动窗口，窗口1次移动1位，你需要在移动过程中计算当前窗口内的最大值。你只能看到当前窗口内的数字。

#### 思路

创建优先队列，队列中元素从大到小排序。接下来力扣评论区提供了一种理解的思路：企业优化裁员的思路。  

- 如果老员工年龄超过35岁（元素离开窗口），直接裁掉；
- 如果老员工能力比新员工能力弱（数值更小），裁掉；

最后留下来的就是按能力（数值）排好序的相对年轻的员工队列啦，队列顶部的元素就是当前窗口内的最大值。

#### 代码

```python
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        # 创建优先队列，python中是小根堆，通过对值取负达到大根堆的效果
        n = len(nums)
        q = [(-nums[i], i) for i in range(k)]
        heapq.heapify(q)

        ans  = [-q[0][0]]
        for i in range(k, n):
            heapq.heappush(q, (-nums[i], i))
            while q[0][1] <= i-k:
                a = heapq.heappop(q)
            ans.append(-q[0][0])
        
        return ans
```

### 76题，#子串，#哈希表，#字符串，#滑动窗口，最小覆盖子串

#### 题目

给定两个字符串s和t，长度分别为m和n，在s中找到一个最短的子串，该子串包含t的所有字符（包含重复字符），找不到的话返回空串，如果有的话保证答案唯一。

#### 思路

这道题仍然使用滑动窗口来做，思路和438题基本一致，

- 计数板：记录窗口中各个字母个数和模版串中的差异。比如：缺失2个'a'、多出来3个'b' 记为 {'a': -2, 'b': 3}
- differ: int，这个值用来记录窗口中一共有多少类字母和模版存在差异。比如计数板为 {'a': -2, 'b': 3，'c': 0}，那么differ就等于1，因为只有'a'和这1类字母个数和模版相比还差了几个。和438不同的地方在于，多出来的字母不用管，因为窗口大小没有限制，我们不是在找字母异位词，只要能够覆盖住模版就行。
- 移动窗口：使用for循环移动窗口，更新计数板。同时检查下面2件事：
    - 本次移出窗口的字母，是否刚好消除了一类字母差异；
    - 本次新加入窗口的字母，是否刚好消除了一类字母的差异；
- 在循环中，最后检查是否不再差字母了，如果是，那么就是找出了一种期望情况。
- 在循环中，将局部最优更新到全局最优值中，就得到了最终答案。

#### 代码

```python
class Solution:
    def minWindow(self, s: str, t: str) -> str:

        l = 0
        ans = ""

        m = len(s)
        n = len(t)
        if m < n:
            return ""

        cnt = {}
        for i in range(n):
            cnt[t[i]] = cnt.setdefault(t[i], 0) - 1
        for i in range(n):
            cnt[s[i]] = cnt.setdefault(s[i], 0) + 1

        differ = [ c<0 for c in cnt.values()].count(True)
        if differ == 0:
            return s[0:n]
        
        for i in range(n, m):
            cnt[s[i]] = cnt.setdefault(s[i], 0) + 1
                
            # 当前字母的出现，刚好填满了模版串中对应字母的个数
            if cnt[s[i]] == 0:
                differ -= 1
            
            # 模版串中所有字母的个数，和当前窗口对应字母的个数都相同，
            # 就是找到了一个解

            # 左指针向右移动，缩短窗口使这组解达到局部最优
            while differ == 0:

                # 更新到全局最优解中
                if not ans or i-l+1 < len(ans):
                    ans = s[l:i+1]

                cnt[s[l]] -= 1
                    
                # 移除了该字母，刚好填不满模版串中对应字母的个数
                if cnt[s[l]] == -1:
                    differ += 1
                
                l += 1

        return ans
```

## 第五章 普通数组

### 53题，#动态规划，最大子数组和

#### 题目

给定一个数组，找出一个非空连续子数组，其和最大。只需要返回最大和。

#### 思路

这是一个动态规划的题目。我觉得动态规划和贪心算法的题目都比较有趣。

- 遍历数组，维护一个最大子前缀和，这样我们就能够知道当前位置和前n个连续值，能够构成的最大和是多少了。
- 将局部最优更新到全局最优值，就得到最终结果了。

#### 代码

```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        mx = nums[0]
        pre = nums[0]
        for i in range(1, len(nums)):
            temp = pre + nums[i]
            pre = temp if temp >= nums[i] else nums[i]
            (pre > mx) and (mx := pre)
        return mx
```

### 56题，#数组，#排序，合并区间

#### 题目

给定二维数组表示多个闭区间，你需要将有重叠（边界也算）的区间合并。

#### 思路

- 先将所有区间按左边界从小到大排序
- 接着遍历所有区间，进行简单合并即可

#### 代码

```python
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        if len(intervals) <= 1:
            return intervals
        intervals = sorted(intervals, key=lambda x:x[0])
        res = []
        left, right = intervals[0][0], intervals[0][1]
        for i in range(1, len(intervals)):
            if intervals[i][0] <= right and intervals[i][1] > right:
                right = intervals[i][1]
                continue
            elif intervals[i][0] > right:
                res.append([left, right])
                left, right = intervals[i][0], intervals[i][1]
        if not res:
            res.append([left, right])
        elif left!=res[-1][0]:
            res.append([left, right])
        return res
```





### 189题，#数组，#数学，#双指针，轮转数组

#### 题目

将给定数组向右轮转k个元素。

#### 思路

这道题目的思路比较巧妙，没想到这种思路的话可能代码会非常复杂，要处理很多边界情况。

需要进行3次反转：

- 将整个列表反转；
- 将前k个反转；
- 将剩下的反转；

这样就得到正确答案了，自己手写一个列表操作一下能很快明白。

#### 代码

```python
class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        k = k % len(nums)
        if k == 0:
            return

        self.rotate_sub(nums, 0, len(nums))
        self.rotate_sub(nums, 0, k)
        self.rotate_sub(nums, k, len(nums)-k)
        
    def rotate_sub(self, nums: List[int], start:int, length: int) -> None:
        for cnt in range(int(length/2)):
            j = start + length - cnt -1
            temp = nums[j]
            nums[j] = nums[start+cnt]
            nums[start+cnt] = temp
```

### 238题，#数组，#前缀和，除了自身以外数组的乘积

#### 题目

给定一个数组，计算每个元素一个对应的乘积，对应的乘积等于除了这个元素之外，其余所有元素的乘积，不能使用除法。

#### 思路

思路就在题干中了，需要两次遍历。

先从前往后遍历，得到每个元素前缀的乘积，再从后往前遍历，得到每个元素所有后缀的乘积。

每个元素的对应乘积=前缀乘积x后缀乘积。

#### 代码

```python
class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        sum_head = [1]*len(nums)
        sum_tail = [1]*len(nums)
        res = []
        for i in range(1, len(nums)):
            sum_head[i] = sum_head[i-1] * nums[i-1]
            sum_tail[len(nums)-i-1] = sum_tail[len(nums)-i] * nums[len(nums)-i]
        for i in range(len(nums)):
            res.append(sum_head[i]*sum_tail[i])
        return res
```

### 41题，#数组，#哈希表，缺失的第一个正数

#### 题目

给定一个整数数组，找出其中未出现的最小正整数。要求时间复杂度是O(n)且只能使用常数级别的额外空间。

#### 思路

这个题目的解法也是一种巧妙的解法，没想到的话面对题干的约束条件就无从下手了。思路有以下几点：

- 将信息直接记录到原数组中；
- 对于一个包含100个元素的数组，如果里面出现了比方说105这个元素，就说明要求的最小正整数一定小于等于100；
- 如果第1个元素是1，第2个元素是2，……，第100个元素是100，那么最小正整数只能是101；
- 基于上面这种思路，我们先遍历一遍数组，将对应的元素值放到对应的下标位置上，由于下标从0开始，所以值为i的元素应该放到下标为i-1的位置上，如果元素值超过下标范围，就不用管；
- 遍历第二遍的时候，我们只要找到下标和值不匹配的位置，就知道最小正整数是多少了。

#### 代码

```python
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        length = len(nums)
        for i in range(length):
            while 1 <= nums[i] <= length and nums[nums[i]-1] != nums[i]:
                nums[nums[i]-1], nums[i] = nums[i], nums[nums[i]-1]
        for i in range(length):
            if nums[i] != i+1:
                return i+1
        return length + 1
```

## 第六章 矩阵

### 73题，#矩阵，#数组，#哈希表，矩阵置换

#### 题目

给定一个矩阵，如果某个位置元素为零，该行和列全部置零。请使用原地算法。

#### 思路

- 第一行用来标记当前列需不需要被清空

- 第一列用来标记当前行需不需要被清空

- 第一个元素被用了两次，所以单独设置一个变量标记第一行需不需要清空

#### 代码

```python
class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """
        m, n  = len(matrix), len(matrix[0])  # m行n列

        # 第一行用来记录当前列需不需要被清空
        # 第一列用来记录当前行需不需要被清空
        # 第一个元素被用了两次，所以单独设置一个变量标记第一行需不需要清空
        row1 = 1 # 0表示需要清空

        # 计算第一行需不需要清空
        for num in matrix[0]:
            if num == 0:
                row1 = 0
                break
        
        # 计算哪些列需要被清空
        for j in range(n):
            for i in range(m):
                if matrix[i][j] == 0:
                    matrix[0][j] = 0
                    break

        # 计算哪些行需要被清空
        for i in range(1, m):
            for j in range(n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    break
        
        # 将对应的行和列清空
        for i in range(1, m):
            for j in range(1, n):
                if matrix[0][j] == 0 or matrix[i][0] == 0:
                    matrix[i][j] = 0
        
        # 判断及清空第一列
        if matrix[0][0] == 0:
            for i in range(m):
                matrix[i][0] = 0
        
        # 判断及清空第一行
        if row1 == 0:
            for j in range(n):
                matrix[0][j] = 0
```

### 54题，#矩阵，#模拟，螺旋矩阵

#### 题目

给定一个矩阵，返回一个列表，由矩阵元素按顺时针螺旋顺序排列组成。

![螺旋矩阵](./assets/spiral.jpg)

图-螺旋矩阵

#### 思路

- 一圈一圈地遍历

- 记录当前这一圈的上下左右下标
- 每一圈分上、右、下、左的顺序4部分分别遍历

#### 代码

```python
class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:

        m, n = len(matrix), len(matrix[0])  # 矩阵为m行n列
        left, right, up, down = 0, n-1, 0, m-1
        locate = 0  # 0，1，2，3分别表示，当前遍历是在上右下左
        ans = []
        while left <= right and up <= down:
            match locate:
                case 0:  # 上
                    for j in range(left, right+1):
                        ans.append(matrix[up][j])
                    up += 1
                case 1:  # 右
                    for i in range(up, down+1):
                        ans.append(matrix[i][right])
                    right -= 1
                case 2:  # 下
                    for j in range(right-left+1):
                        ans.append(matrix[down][right-j])
                    down -= 1
                case 3:  # 左
                    for i in range(down-up+1):
                        ans.append(matrix[down-i][left])
                    left += 1
            locate = (locate + 1) % 4
        
        return ans
```

### 48题，#矩阵， 旋转图像

#### 题目

给定一个矩阵，将矩阵顺时针旋转。你需要原地旋转。

![旋转图像](./assets/mat2.jpg)

图-旋转图像

#### 思路

- 一圈一圈转
- 转的时候按照观察到的简单的数学规律转一圈即可

#### 代码

```python
class Solution:
    def rotate(self, matrix: List[List[int]]) -> None:
        """
        Do not return anything, modify matrix in-place instead.
        """

        if len(matrix) <= 1:
            return

        interval, a, b, c, d = 0, 0, 0, 0, 0

        for i in range(int(len(matrix)/2)):  # 从第一圈到最后一圈
            interval = len(matrix) - 2 * i - 1 # 一行的长度（前闭后开）
            # 绕一圈，将所有数字换一下
            for j in range(interval):
                a = matrix[i][i+j]
                b = matrix[i+j][i+interval]
                c = matrix[i+interval][i+interval-j]
                d = matrix[i+interval-j][i]

                matrix[i][i+j] = d  # a = d
                matrix[i+j][i+interval] = a  # b = a 
                matrix[i+interval][i+interval-j] = b  # c = b
                matrix[i+interval-j][i] = c  # d = c
```

### 240题，#矩阵，搜索二维矩阵II

#### 题目

给定一个矩阵，该矩阵从左到右、从上到下都是升序。你需要判断该矩阵有没有包含指定值。

#### 思路

- 利用矩阵升序的规律，从左下角开始找

- 如果m\[x][y] == target: 好事

- 如果m\[x][y] < target: y →

- 如果m\[x][y] > target: x ↑

- 如果x < 0 or y >= n: 坏事

#### 代码

```python
class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        # 从左下角开始找
        # 如果m[x][y] == target: 好事
        # 如果m[x][y] < target: y →
        # 如果m[x][y] > target: x ↑
        # 如果x < 0 or y >= n: 坏事
        m, n = len(matrix), len(matrix[0])
        x, y = m-1, 0
        while x >= 0 and y < n:
            if matrix[x][y] == target:
                return True
            elif matrix[x][y] < target:
                y += 1
            else:
                x -= 1
        return False
```

## 第七章 链表

### 160题，#链表，#哈希表，相交链表

#### 题目

返回两个链表的交点，不存在就返回null。

#### 思路

遍历链表A，所有结点存进哈希表中。接着遍历链表B，第一个存在于哈希表中的结点就是交点。

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, x):
##         self.val = x
##         self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> Optional[ListNode]:
        setA = set()
        while headA:
            setA.add(headA)
            headA = headA.next
        while headB:
            if headB in setA:
                return headB
            headB = headB.next
        return None
```

### 206题，#链表，反转链表

#### 题目

将一个链表反转。

#### 思路

将链表从前往后遍历，将遍历到的结点不断接在新的头结点前面。

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, val=0, next=None):
##         self.val = val
##         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        newHead = None
        temp = None
        while head:
            temp = head.next
            head.next = newHead
            newHead = head
            head = temp
        return newHead
```

### 234题，#链表，#双指针，回文链表

#### 题目

判断一个链表是否回文。

#### 思路

取链表中点，将前半段反转，比较前后两半段是否相同。

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, val=0, next=None):
##         self.val = val
##         self.next = next
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:

        # 计算回文的中点
        lHead = None
        rHead = None
        temp = None
        newHead = head
        total = 0
        while(newHead):
            total += 1
            newHead = newHead.next
        cnt = int(total / 2)
        
        # 特殊情况处理
        if total <= 1:
            return True
            
        # 将回文左半边翻转
        lHead = head
        newHead = None
        temp = None
        for i in range(cnt):
            temp = head.next
            head.next = newHead
            newHead = head
            head = temp
        lHead = newHead

        # 计算右边的起点
        if total % 2 == 1:
            rHead = temp.next
        else:
            rHead = temp
        
        # 比较两边是否等价
        while(rHead):
            print(f"lHead:{lHead.val}, rHead:{rHead.val}")
            if lHead.val != rHead.val:
                return False
            lHead = lHead.next
            rHead = rHead.next
        
        return True
```

### 141题，#链表，#快慢指针，环形链表

#### 题目

判断一个链表是否有环。

#### 思路

有两种思路：

- ① 哈希表：遍历链表，结点存进哈希表中，如果结点已经存在于哈希表中，就是有环
- ② 「Floyd判圈算法」（又称龟兔赛跑算法）：一个快指针1次走2步，一个慢指针1次走1步，没有环的话快指针会一直走在前面直到null，如果快指针反而从后面追上慢指针，说明存在环。

在判圈算法中，快慢指针一定会相遇，可以通过公式推导，在下一题会给出。

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, x):
##         self.val = x
##         self.next = None

class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        nset = set()
        while head:
            if head in nset:
                return True
            nset.add(head)
            head = head.next
        return False
```

### 142题，#链表，#快慢指针，环形链表II

#### 题目

返回链表中开始入环的第一个起点，无环就返回null。

![环形链表](./assets/circularlinkedlist.png)

图-环形链表II

#### 思路

和上一题一样的两种思路，这里给出判圈算法的公式，求解何时会相遇。

![判圈算法](./assets/142_fig1.png)

图-判圈算法

定义快慢指针slow和fast，都从下标0出发，慢指针1次1步，快指针1次2步。

当快慢指针相遇时，假设相遇在紫色点位置，我们有：

fast移动距离 = a+n(b+c)+b = a+(n+1)b+nc = 2(a+b) = 2 x (slow移动距离)

 从上面公式我们可以推导出 a = c+(n-1)(b+c)，当快慢指针相遇的时候，我们让一个新的慢指针ptr从头开始走，同时原先的慢指针slow继续前进，最终ptr和slow一定会在环的入口处相遇，此时，slow继续走了(n-1)圈+c步，走到了环入口处，ptr走了a。

于是，就找到了环入口处。

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, x):
##         self.val = x
##         self.next = None

class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        nset = set()
        newHead = head
        x = None
        while(newHead):
            if newHead in nset:
                x = newHead
                break
            nset.add(newHead)
            newHead = newHead.next
        return x
```

### 21题，#链表，#递归，合并两个有序链表

#### 题目

将两个升序链表合并成一个升序链表。

#### 思路

- ans：要返回的链表头指针，添加头结点可以统一操作；
- 使用两个指针分别遍历两个链表即可；

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, val=0, next=None):
##         self.val = val
##         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:

        curr = ans = ListNode()  # 带头结点

        if not list1 or not list2:
            return list1 if list1 else list2

        while list1 or list2:
            if not list1:  # list1没了
                curr.next = list2
                list2 = list2.next
            elif not list2:  # list2没了
                curr.next = list1
                list1 = list1.next
            elif list1.val < list2.val:  # list1小，先list1
                curr.next = list1
                list1 = list1.next
            else:  # list2小（或等于），先list2
                curr.next = list2
                list2 = list2.next
            curr = curr.next
        
        return ans.next  # 去掉头结点后返回
```

### 2题，#链表，#递归，两数相加

#### 题目

两个非空链表表示两个整数，对这两个整数求和，保存为第三个链表并返回。

![链表两数相加](./assets/addtwonumber1.jpg)

图-链表两数相加

#### 思路

- 头结点：返回的链表先加个头结点，好操作；
- 接着正常按位相加即可，同时判断有没有进位；

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, val=0, next=None):
##         self.val = val
##         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        ans = None
        cur = None
        carry = 0
        while(l1 or l2):
            l1_val = l2_val = 0
            if l1:
                l1_val = l1.val
                l1 = l1.next
            if l2:
                l2_val = l2.val
                l2 = l2.next
            sub = l1_val + l2_val + carry
            carry = int(sub / 10)
            sub = int(sub % 10)
            if not ans:
                ans = cur = ListNode(val=sub)
            else:
                temp = ListNode(val=sub)
                cur.next = temp
                cur = temp
        if carry:
                temp = ListNode(val=carry)
                cur.next = temp
                cur = temp

        return ans
```

### 19题，#链表，#快慢指针，删除链表的倒数第N个结点

#### 题目

给定一个链表，删除链表的倒数第N个结点。

#### 思路

快慢指针，两个指针分别从下标0和下标N开始遍历链表，当右指针到达链表末尾的时候，左指针就指着倒数第N的位置，把它删了即可。

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, val=0, next=None):
##         self.val = val
##         self.next = next
class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        
        # 计算有多少个结点
        total = 0
        curr = head
        while(curr):
            total += 1
            curr = curr.next
        
        # 特殊情况处理
        if total <= 1:
            return None

        
        if total == n:
            return head.next

        # 删除对应的结点
        curr = head
        cnt = 1
        while(cnt < total-n):
            curr = curr.next
            cnt += 1
        
        if curr:
            curr.next = curr.next.next
        return head
```

### 24题，#链表，#快慢指针，两两交换链表中的结点

#### 题目

给定一个链表，两两交换其中相邻的结点。你不能改变结点内部的值。

#### 思路

- 头结点：添加头结点统一操作
- 3个指针：记录当前相关的三个指针，然后做交换就可以了

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, val=0, next=None):
##         self.val = val
##         self.next = next
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        head = ListNode(next=head)
        curr = head
        n1 = n2 = n3 = None
        while(curr.next and curr.next.next):
            n1 = curr.next
            n2 = n1.next
            n3 = n2.next
            curr.next = n2
            n2.next = n1
            n1.next = n3
            curr = curr.next.next
        return head.next
```

### 25题，#链表，#快慢指针，K个一组翻转链表

#### 题目

给定一个链表，按照链表中k个一组翻转链表。

#### 思路

- 头结点：添加头结点统一操作

- 4个结点：记录段边界的4个结点，进行局部翻转即可。

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, val=0, next=None):
##         self.val = val
##         self.next = next
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        
        # 特殊情况处理
        if k == 1 or not head:
            return head

        head = ListNode(next=head) # 设置一个
        hout = head # 该段的前一个结点
        hin = head.next # 该段的第一个结点
        tin = None # 该段的最后一个结点
        tout = None # 该段的后一个结点
        curr = head
        cnt = 0
        end = None

        # 分段翻转
        while(1):

            # 找到往后第k个
            cnt = 1
            tin = hin
            while(cnt < k and tin):
                tin = tin.next
                cnt += 1

            # 如果剩下的结点少于k个就退出
            if not tin:
                break

            tout = tin.next
            
            hin, tin = self.reverse(hin, tin)
            hout.next = hin
            tin.next = tout
            hout = tin
            hin = tout

        return head.next

            
    def reverse(self, hin, tin):
        
        curr = hin
        newstart = None
        tout = tin.next
        while(curr != tout):
            temp = curr.next
            curr.next = newstart
            newstart = curr
            curr = temp
        hin.next = tout
        return newstart, hin
```

### 138题，#链表，#哈希表，随机链表的复制

#### 题目

给定一个链表，每个节点增加了一个随机指针，像下图这样，你要做的是，对链表做深拷贝。

![随机链表复制](./assets/e1.png)

图-随机链表复制

#### 思路

- 哈希表：遍历第一遍，为原来的所有节点创建副本，映射关系保存到字典
- 遍历第二遍：按照字典，将原链表结点对应的副本之间的下指针和随机指针捋一遍
- 完成

#### 代码

```python
"""
## Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        curr = head
        mp = {}
        while curr:
            mp[curr] = Node(x=curr.val)
            curr = curr.next

        curr = head
        while curr:
            mp[curr].next = mp[curr.next] if curr.next else None
            mp[curr].random = mp[curr.random] if curr.random else None
            curr = curr.next
        
        return mp[head] if head else None
```

### 148题，#链表，#快慢指针，#归并排序，排序链表

#### 题目

给定一个链表，你将它按归并排序。

#### 思路

- 二分法：用快慢指针找链表中点，慢指针1次走1步，快指针1次走2步
- 递归，在递归中对左右两段链表排序，也就是归并排序

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, val=0, next=None):
##         self.val = val
##         self.next = next
class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        # 递归推出条件
        if not head or not head.next:
            return head

        # 将链表切分成两段
        slow, fast = head, head.next
        while fast and fast.next:
            slow, fast = slow.next, fast.next.next
        mid, slow.next = slow.next, None

        # 递归切分并内部排序
        left, right = self.sortList(head), self.sortList(mid)

        # 将分别排好序的左右两段归并到一起
        curr = res = ListNode(0)
        while left and right:
            if left.val < right.val:
                curr.next = left
                left = left.next
            else:
                curr.next = right
                right = right.next
            curr = curr.next
        
        curr.next = left if left else right

        return res.next
```

### 23题，#链表，#分治，#堆（优先队列），合并K个升序链表

#### 题目

给定一个链表组，组中每个链表已经各自按升序排序，你将链表组中所有链表合并成一个升序链表。

```
输入：lists = [[1,4,5],[1,3,4],[2,6]]
输出：[1,1,2,3,4,4,5,6]
```

#### 思路

将链表组中2个链表一组做归并排序，完成。思路和上一题148题本质上是一样的。

#### 代码

```python
## Definition for singly-linked list.
## class ListNode:
##     def __init__(self, val=0, next=None):
##         self.val = val
##         self.next = next
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        
        cnt, total = 0, len(lists)
        while total > 1:
            for i in range(0, int(total/2)):
                merged = self.merge2Lists(lists[2*i], lists[2*i+1])
                lists[cnt] = merged
                cnt += 1
            if total % 2 == 0:
                total = cnt
            else:
                lists[cnt] = lists[total-1]
                total = cnt + 1
            cnt = 0
        
        return lists[0]
            


    def merge2Lists(self, la: List[Optional[ListNode]], lb: List[Optional[ListNode]]) -> Optional[ListNode]:

        curr = res = ListNode(0)
        while la and lb:
            if la.val < lb.val:
                curr.next = la
                la = la.next
            else:
                curr.next = lb
                lb = lb.next
            curr = curr.next
        curr.next = la if la else lb
        return res.next
```

## 第八章 二叉树

### 94题，#二叉树，二叉树的中序遍历

#### 题目

给定一个二叉树，进行中序遍历，返回`val`列表

#### 思路

就是中序遍历，把最后要返回的列表指针在递归中一层层传进去。

### 代码

```python
## Definition for a binary tree node.
## class TreeNode:
##     def __init__(self, val=0, left=None, right=None):
##         self.val = val
##         self.left = left
##         self.right = right
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        def dfs(root: Optional[TreeNode], res: List[int]):
            if not root:
                return
            root.left and dfs(root.left, res)
            res.append(root.val)
            root.right and dfs(root.right, res)
        
        res = []
        dfs(root,res)
        return res
```



### 104题，#二叉树，#递归，二叉树的最大深度

#### 题目

给定一个二叉树，计算其最大深度

#### 思路

递归就行了。

### 代码

```python
## Definition for a binary tree node.
## class TreeNode:
##     def __init__(self, val=0, left=None, right=None):
##         self.val = val
##         self.left = left
##         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        # 递归
        if not root:
            return 0
        ln = self.maxDepth(root.left) + 1
        rn = self.maxDepth(root.right) + 1
        
        return max(ln, rn)
```



### 226题，#二叉树，#递归，翻转二叉树

#### 题目

给定二叉树，进行镜像翻转，返回根节点。

#### 思路

递归就行了。

### 代码

```python
## Definition for a binary tree node.
## class TreeNode:
##     def __init__(self, val=0, left=None, right=None):
##         self.val = val
##         self.left = left
##         self.right = right
class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        # 递归
        if not root:
            return root
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root
```



### 101题，#二叉树，#递归，对称二叉树

#### 题目

给定二叉树，判断其是否左右对称。

#### 思路

递归就行了。

#### 代码

```python
## Definition for a binary tree node.
## class TreeNode:
##     def __init__(self, val=0, left=None, right=None):
##         self.val = val
##         self.left = left
##         self.right = right
class Solution:
    def isSymmetric(self, root: Optional[TreeNode]) -> bool:
        if not root:
            return True
        
        return self.isEqual(root.left, root.right)
        
    def isEqual(self, left: Optional[TreeNode], right: Optional[TreeNode]) -> bool:
        if not left and not right:
            return True
        if not left or not right:
            return False
        if left.val != right.val:
            return False
        
        return self.isEqual(left.left, right.right) and self.isEqual(left.right, right.left)
```

### 543题，#二叉树，#深度优先搜索，二叉树的直径

#### 题目

给定一个二叉树，计算二叉树中最长路径的边数，可以不经过根节点。

#### 思路

用递归做一次深度优先搜索，更新全局最大值即可。

#### 代码

```python
## Definition for a binary tree node.
## class TreeNode:
##     def __init__(self, val=0, left=None, right=None):
##         self.val = val
##         self.left = left
##         self.right = right
class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        self.mx = 0
        def mxPath(root: Optional[TreeNode]) -> int:
            if not root:
                return 0
            
            ln = 1 + mxPath(root.left) if root.left else 0
            rn = 1 + mxPath(root.right) if root.right else 0
            self.mx = max(ln+rn, self.mx)
            return max(ln, rn)
        
        mxPath(root)
        return self.mx
```

### 102题，#二叉树，#广度优先搜索，二叉树的层序遍历

#### 题目

给定一个二叉树，做一次层序遍历。

#### 思路

就是层序遍历，用队列。

#### 代码

```python
## Definition for a binary tree node.
## class TreeNode:
##     def __init__(self, val=0, left=None, right=None):
##         self.val = val
##         self.left = left
##         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        ans = []
        cur = [root]
        curv = [root.val]
        nxt = []
        nxtv = []
        while(cur):
            ans.append(curv)

            for node in cur:
                if node.left:
                    nxt.append(node.left)
                    nxtv.append(node.left.val)
                if node.right:
                    nxt.append(node.right)
                    nxtv.append(node.right.val)
            
            cur, curv, nxt, nxtv = nxt, nxtv, [], []
        return ans
```



## 第九章 图论



## 第十章 回溯



## 第十一章 二分查找



## 第十二章 栈



### 20题，#栈，#括号匹配，有效的括号

#### 题目

给定一个字符串，是一个括号序列，检查序列中的括号是否正确配对、闭合，不用管大中小括号之类的顺序嵌套（小括号中可以包含大括号）。

#### 思路

遍历一遍，内部遇到左括号就push进栈，遇到右括号就从栈中pop出栈检查是否配对即可。

#### 代码

```python
class Solution:
    def isValid(self, s: str) -> bool:
        stack = []  # 用来保存待匹配的栈
        left_ps = ['(', '[', '{']
        right_ps = [')', ']', '}']
        for char in s:
            if char in left_ps:
                stack.append(char)
            elif char in right_ps:
                if not stack:
                    return False
                left_p = stack.pop()
                if left_p == '(' and not char == ')':
                    return False
                elif left_p == '[' and not char == ']':
                    return False
                elif left_p == '{' and not char == '}':
                    return False
        if stack:
            return False
        return True
```



### 155题，#栈，最小栈

#### 题目

实现一个最小栈，需要保存元素的入栈顺序信息，还需要在常数时间内获取栈内元素的最小值。

#### 思路

使用两个栈：元素栈、辅助栈。

- 元素栈：按入栈顺序存放元素
- 辅助栈：每一时刻元素栈中的最小值

#### 代码

```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = [math.inf]

    def push(self, x: int) -> None:
        self.stack.append(x)
        self.min_stack.append(min(x, self.min_stack[-1]))

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]

作者：力扣官方题解
链接：https://leetcode.cn/problems/min-stack/solutions/
来源：力扣（LeetCode）
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```





## 第十三章 堆



## 第十四章 贪心算法



## 第十五章 动态规划



## 第十六章 多维动态规划



## 第十七章 技巧



# 剑指offer
