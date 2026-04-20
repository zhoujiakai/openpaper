# Attention Is All You Need

> Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin
> Google Brain / Google Research / University of Toronto
> arXiv:1706.03762v7

---

## Abstract

The dominant sequence transduction models are based on complex **recurrent neural networks** or **convolutional neural networks** that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an **attention mechanism**.

We propose a new simple network architecture, the **Transformer**, based entirely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train.

Our model achieves **28.4 BLEU** on the **WMT 2014 English-to-German** translation task, improving over the existing best results, including ensembles, by over 2 BLEU. On the **WMT 2014 English-to-French** translation task, our model establishes a new single-model state-of-the-art BLEU score of **41.8** after training on **8 GPUs for 3.5 days**, a small fraction of the training costs of the best models from the literature.

We show that the Transformer generalizes well to other tasks by applying it successfully to **English constituency parsing** both with large and limited training data.

---

## 1 Introduction

**Recurrent neural networks**, long short-term memory [13] and **gated recurrent** [7] neural networks in particular, have been firmly established as state of the art approaches in sequence modeling and transduction problems such as language modeling and machine translation [35, 2, 5]. Numerous efforts have since continued to push the boundaries of recurrent language models and encoder-decoder architectures [38, 24, 15].

Recurrent models typically factor computation along the symbol positions of the input and output sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden states $h_t$, as a function of the previous hidden state $h_{t-1}$ and the input for position $t$. This inherently sequential nature precludes parallelization within training examples, which becomes critical at longer sequence lengths, as memory constraints limit batching across examples.

Recent work has achieved significant improvements in computational efficiency through **factorization tricks** [21] and **conditional computation** [32], the latter also improving model performance. The fundamental constraint of sequential computation, however, remains.

**Attention mechanisms** have become an integral part of compelling sequence modeling and transduction models in various tasks, allowing modeling of dependencies without regard to their distance in the input or output sequences [2, 19]. In all but a few cases [27], however, such attention mechanisms are used in conjunction with a recurrent network.

In this work we propose the **Transformer**, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as **12 hours on 8 P100 GPUs**.

---

## 2 Background

The goal of reducing sequential computation also forms the foundation of the **Extended Neural GPU** [16], **ByteNet** [18], and **ConvS2S** [9], all of which use convolutional neural networks as basic building blocks, computing hidden representations in parallel for all input and output positions.

In these models, the number of operations required to relate signals from two arbitrary input or output positions grows in the distance between positions — **linearly** for ConvS2S and **logarithmically** for ByteNet. This makes it more difficult to learn dependencies between distant positions [12].

> In the Transformer this is reduced to a **constant number of operations**, albeit at the cost of reduced effective resolution due to averaging attention-weighted positions — an effect we counteract with **Multi-Head Attention** (Section 3.2).

**Self-attention**, sometimes called intra-attention, is an attention mechanism relating different positions of a single sequence in order to compute a representation of the sequence. Self-attention has been used successfully in a variety of tasks including reading comprehension, abstractive summarization, textual entailment, and learning task-independent sentence representations [4, 27, 28, 22].

**End-to-end memory networks** are based on a recurrent attention mechanism instead of sequence-aligned recurrence and have been shown to perform well on simple-language question answering and language modeling tasks [34].

To the best of our knowledge, however, **the Transformer is the first transduction model relying entirely on self-attention** to compute representations of its input and output without using sequence-aligned RNNs or convolution.

---

## 3 Model Architecture

<img src="assets/ModalNet-21.png" alt="Figure 1: The Transformer - model architecture" width="380" />

**Figure 1:** The Transformer - model architecture. Left: encoder, right: decoder.

Most competitive neural sequence transduction models have an **encoder-decoder** structure [5, 2, 35]. Here, the encoder maps an input sequence of symbol representations $(x_1, ..., x_n)$ to a sequence of continuous representations $\mathbf{z} = (z_1, ..., z_n)$. Given $\mathbf{z}$, the decoder then generates an output sequence $(y_1, ..., y_m)$ of symbols one element at a time. At each step the model is **auto-regressive** [10], consuming the previously generated symbols as additional input when generating the next.

The Transformer follows this overall architecture using **stacked self-attention** and **point-wise, fully connected layers** for both the encoder and decoder, shown in the left and right halves of Figure 1, respectively.

---

### 3.1 Encoder and Decoder Stacks

#### Encoder

The encoder is composed of a stack of **N = 6** identical layers. Each layer has two sub-layers:

1. A **multi-head self-attention mechanism**
2. A **position-wise fully connected feed-forward network**

We employ a **residual connection** [11] around each of the two sub-layers, followed by **layer normalization** [1]. That is, the output of each sub-layer is:

```
LayerNorm(x + Sublayer(x))
```

To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension **d_model = 512**.

#### Decoder

The decoder is also composed of a stack of **N = 6** identical layers. In addition to the two sub-layers in each encoder layer, the decoder inserts a **third sub-layer**, which performs multi-head attention over the output of the encoder stack.

Similar to the encoder, we employ residual connections around each of the sub-layers, followed by layer normalization. We also modify the self-attention sub-layer in the decoder stack to **prevent positions from attending to subsequent positions**. This **masking**, combined with the fact that the output embeddings are offset by one position, ensures that the predictions for position $i$ can depend only on the known outputs at positions less than $i$.

---

### 3.2 Attention

An attention function can be described as mapping a **query** and a set of **key-value pairs** to an output, where the query, keys, values, and output are all vectors. The output is computed as a weighted sum of the values, where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key.

#### 3.2.1 Scaled Dot-Product Attention

<img src="assets/ModalNet-19.png" alt="Figure 2 (left): Scaled Dot-Product Attention" width="150" />

We call our particular attention "**Scaled Dot-Product Attention**" (Figure 2, left). The input consists of queries and keys of dimension $d_k$, and values of dimension $d_v$.

Computation:

```
1. Compute the dot products of the query with all keys
2. Divide each by √d_k
3. Apply a softmax function to obtain the weights on the values
4. Multiply the values by the weights and sum
```

Formula:

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V \quad (1)$$

The two most commonly used attention functions are:

| Type | Principle | Characteristics |
|------|-----------|-----------------|
| **Additive attention** | Computes compatibility using a feed-forward network with a single hidden layer | Similar theoretical complexity |
| **Dot-product attention** | Computes the dot product directly | Faster, more space-efficient |

> Why scaling? When $d_k$ is large, the dot products grow large in magnitude, pushing the softmax function into regions with extremely small gradients. To illustrate why, assume the components of $q$ and $k$ are independent random variables with mean 0 and variance 1. Then their dot product $q \cdot k = \sum_{i=1}^{d_k} q_i k_i$ has mean 0 and variance $d_k$. To counteract this, we scale the dot products by $1/\sqrt{d_k}$.

#### 3.2.2 Multi-Head Attention

<img src="assets/ModalNet-20.png" alt="Figure 2 (right): Multi-Head Attention" width="280" />

Instead of performing a single attention function with $d_{\text{model}}$-dimensional keys, values and queries, it is found to be beneficial to:

```
1. Linearly project the queries, keys and values h times with different,
   learned linear projections to d_k, d_k and d_v dimensions, respectively
2. Perform the attention function in parallel on each of these projected versions
3. Yield d_v-dimensional output values for each head
4. Concatenate them
5. Once again project with a final linear layer to produce the final result
```

Formula:

$$\text{MultiHead}(Q, K, V) = \text{Concat}(\text{head}_1, ..., \text{head}_h)W^O$$

where:

$$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$$

The projection matrices: $W_i^Q \in \mathbb{R}^{d_{\text{model}} \times d_k}$, $W_i^K \in \mathbb{R}^{d_{\text{model}} \times d_k}$, $W_i^V \in \mathbb{R}^{d_{\text{model}} \times d_v}$, $W^O \in \mathbb{R}^{hd_v \times d_{\text{model}}}$

> **In this work**: h = **8** parallel attention heads. For each of these, $d_k = d_v = d_{\text{model}} / h = 64$. Due to the reduced dimension of each head, the **total computational cost is similar to that of single-head attention with full dimensionality**.

**Significance of multi-head attention**: Multi-head attention allows the model to jointly attend to information from **different representation subspaces** at **different positions**. With a single attention head, averaging inhibits this.

#### 3.2.3 Applications of Attention in our Model

The Transformer uses multi-head attention in **three different ways**:

1. **Encoder-decoder attention layers**
   - Queries come from the previous decoder layer
   - Keys and values come from the output of the encoder
   - This allows every position in the decoder to attend over all positions in the input sequence
   - This mimics the typical encoder-decoder attention mechanisms in sequence-to-sequence models

2. **Encoder self-attention layers**
   - In the encoder, all of the keys, values and queries come from the output of the previous layer in the encoder
   - Each position in the encoder can attend to all positions in the previous layer of the encoder

3. **Decoder self-attention layers**
   - Allows each position in the decoder to attend to all positions in the decoder up to and including that position
   - **We need to prevent leftward information flow** to preserve the auto-regressive property
   - We implement this by masking out (setting to $-\infty$) all values in the input of the softmax that correspond to illegal connections

---

### 3.3 Position-wise Feed-Forward Networks

In addition to attention sub-layers, each of the layers in our encoder and decoder contains a **fully connected feed-forward network**, which is applied to each position **separately and identically**.

This consists of two linear transformations with a **ReLU** activation in between:

$$\text{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2 \quad (2)$$

While the linear transformations are the same across different positions, they **use different parameters from layer to layer**. Another way of describing this is as two convolutions with kernel size 1.

- Input and output dimensionality: $d_{\text{model}} = 512$
- Inner-layer dimensionality: $d_{ff} = 2048$

---

### 3.4 Embedding and Softmax

Similarly to other sequence transduction models:

- We use **learned embeddings** to convert the input tokens and output tokens to vectors of dimension $d_{\text{model}}$
- We use the **learned linear transformation** and **softmax function** to convert the decoder output to predicted next-token probabilities
- In our model, we **share the same weight matrix** between the two embedding layers and the pre-softmax linear transformation (similar to [30])
- In the embedding layers, we multiply those weights by $\sqrt{d_{\text{model}}}$

---

### 3.5 Positional Encoding

Since our model contains **no recurrence and no convolution**, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence.

To this end, we add **positional encodings** to the input embeddings at the bottoms of the encoder and decoder stacks. The positional encoding has the same dimension $d_{\text{model}}$ as the embeddings, so that the two can be summed.

In this work, we use **sine and cosine functions** of different frequencies:

$$PE_{(pos, 2i)} = \sin(pos / 10000^{2i/d_{\text{model}}})$$
$$PE_{(pos, 2i+1)} = \cos(pos / 10000^{2i/d_{\text{model}}})$$

where $pos$ is the position and $i$ is the dimension. Each dimension of the positional encoding corresponds to a sinusoid. The wavelengths form a **geometric progression** from $2\pi$ to $10000 \cdot 2\pi$.

> **Why this function?** We hypothesized it would allow the model to easily learn to attend by relative positions, since for any fixed offset $k$, $PE_{pos+k}$ can be represented as a linear function of $PE_{pos}$.

We also experimented with **learned positional embeddings** [9], and found that the two versions produced nearly identical results (Table 3 row (E)). We chose the sinusoidal version because it may allow the model to **extrapolate** to sequence lengths longer than those encountered during training.

---

## 4 Why Self-Attention

In this section we compare various aspects of self-attention layers to the recurrent and convolutional layers commonly used for mapping one variable-length sequence of symbol representations to another sequence of equal length.

We consider three motivating factors:

| Metric | Meaning |
|--------|---------|
| **Total computational complexity per layer** | The total amount of computation in a layer |
| **Amount of computation that can be parallelized** | Measured by the minimum number of sequential operations required |
| **Path length between long-range dependencies** | The maximum path length between any two positions in the network |

**Table 1: Comparison of different layer types**

| Layer Type | Complexity per Layer | Sequential Operations | Maximum Path Length |
|-----------|---------------------|----------------------|---------------------|
| **Self-Attention** | $O(n^2 \cdot d)$ | $O(1)$ | $O(1)$ |
| **Recurrent** | $O(n \cdot d^2)$ | $O(n)$ | $O(n)$ |
| **Convolutional** | $O(k \cdot n \cdot d^2)$ | $O(1)$ | $O(n/k)$ |
| Self-Attention (restricted, neighborhood size r) | $O(r \cdot n \cdot d)$ | $O(n/r)$ | $O(n/r)$ |

> $n$ = sequence length, $d$ = representation dimension, $k$ = kernel size, $r$ = neighborhood size for restricted self-attention

Key takeaways:

- A self-attention layer connects all positions with **O(1) sequential operations**, whereas a recurrent layer requires **O(n)** sequential operations
- When the sequence length $n$ is smaller than the representation dimensionality $d$, self-attention layers are **faster** than recurrent layers (as is often the case with machine translation)
- A single convolutional layer with kernel width $k < n$ does not connect all pairs of input and output positions — doing so requires a stack of $O(n/k)$ convolutional layers (for contiguous kernels) or $O(\log_k(n))$ layers (for dilated convolutions)
- **Side benefit**: Self-attention could yield more **interpretable models** — different attention heads clearly learned to perform different tasks

---

## 5 Training

### 5.1 Training Data and Batching

| Task | Dataset | Size | Tokenization | Vocabulary |
|------|---------|------|-------------|-----------|
| En→De | WMT 2014 | ~4.5 million sentence pairs | byte-pair encoding | ~37,000 tokens |
| En→Fr | WMT 2014 | ~36 million sentences | word-piece | 32,000 tokens |

Sentence pairs were batched together by approximate sequence length. Each training batch contained a set of sentence pairs containing approximately **25,000 source tokens** and **25,000 target tokens**.

### 5.2 Hardware and Schedule

- **One machine with 8 NVIDIA P100 GPUs**
- **Base model**: ~0.4 seconds per training step, trained for 100,000 steps (**12 hours**)
- **Big model**: ~1.0 seconds per training step, trained for 300,000 steps (**3.5 days**)

### 5.3 Optimizer

We used **Adam** [20] with $\beta_1 = 0.9$, $\beta_2 = 0.98$, $\epsilon = 10^{-9}$.

We varied the learning rate over the course of training, according to the formula:

$$lrate = d_{\text{model}}^{-0.5} \cdot \min(step\_num^{-0.5},\ step\_num \cdot warmup\_steps^{-1.5}) \quad (3)$$

> This corresponds to increasing the learning rate **linearly for the first warmup_steps training steps**, and decreasing it thereafter **proportionally to the inverse square root of the step number**. We used $warmup\_steps = 4000$.

### 5.4 Regularization

We employed **three types of regularization** during training:

**Residual Dropout**:
- We apply dropout [33] to the output of each sub-layer (before it is added to the sub-layer input and normalized)
- We also apply dropout to the sums of the embeddings and the positional encodings in both the encoder and decoder stacks
- For the base model, we use a rate of $P_{drop} = 0.1$

**Label Smoothing**:
- We employ label smoothing of $\epsilon_{ls} = 0.1$ [36]
- This hurts perplexity, as the model learns to be more unsure, but **improves accuracy and BLEU score**

---

## 6 Results

### 6.1 Machine Translation

**WMT 2014 English-to-German translation**:
- **Big model** BLEU = **28.4**, outperforming the best previously reported models (including ensembles) by over **2.0 BLEU**
- Trained on **8 P100 GPUs for 3.5 days**
- Even the **Base model** surpassed all previously published models and ensembles, at a fraction of the training cost

**WMT 2014 English-to-French translation**:
- Big model BLEU = **41.0**, outperforming all previously published single models
- Training cost less than **1/4** of the previous state-of-the-art model

Inference settings:
- Base model: averaged the last **5** checkpoints (written at 10-minute intervals)
- Big model: averaged the last **20** checkpoints
- Beam search: beam size = **4**, length penalty $\alpha = 0.6$
- Maximum output length: input length + 50, terminated early when possible

### 6.2 Model Variations

We evaluated the importance of different components of the Transformer on the English-to-German translation development set (newstest2013):

**Table 3 key findings**:

| Variation | What changed | Result |
|-----------|-------------|--------|
| **(A)** Number of attention heads | 1/4/16/32 heads | Single-head is 0.9 BLEU less than the best, quality drops with too many heads |
| **(B)** Attention key dimension | Reduced $d_k$ | Reducing key dimension hurts quality |
| **(C)** Model size | Varied layers/dimensions | Larger models are better |
| **(D)** Dropout | 0.0/0.1/0.2 | Dropout is very helpful in preventing overfitting |
| **(E)** Positional encoding | Learned vs. sinusoidal | Results are nearly identical |

**Big model configuration**: N=6, $d_{\text{model}}=1024$, $d_{ff}=4096$, h=16, $P_{drop}=0.3$, **213M parameters**, trained for 300K steps, BLEU **26.4**

### 6.3 English Constituency Parsing

To evaluate whether the Transformer can generalize to other tasks, we performed experiments on **English constituency parsing**.

Challenges of this task:
- Output is subject to **strong structural constraints**
- Output is **significantly longer** than the input
- RNN sequence-to-sequence models have not been able to attain state-of-the-art results on small datasets [37]

Experimental setup:
- 4-layer Transformer with $d_{\text{model}} = 1024$
- **WSJ only**: ~40K training sentences, vocabulary of 16K tokens
- **Semi-supervised**: plus BerkleyParser corpus, ~17M sentences, vocabulary of 32K tokens

Results (Table 4, WSJ Section 23 F1):

| Model | Training | F1 |
|-------|----------|-----|
| Vinyals & Kaiser (2014) [37] | WSJ only | 88.3 |
| Petrov et al. (2006) [29] | WSJ only | 90.4 |
| Dyer et al. (2016) [8] | WSJ only | 91.7 |
| **Transformer (4-layer)** | **WSJ only** | **91.3** |
| McClosky et al. (2006) [26] | Semi-supervised | 92.1 |
| Vinyals & Kaiser (2014) [37] | Semi-supervised | 92.1 |
| **Transformer (4-layer)** | **Semi-supervised** | **92.7** |
| Dyer et al. (2016) [8] | Generative | 93.3 |

> Remarkably, despite having been designed for and trained on a completely different task, the Transformer performs surprisingly well — outperforming the BerkeleyParser even when trained only on the WSJ training set of ~40K sentences, unlike RNN sequence-to-sequence models.

---

## 7 Conclusion

In this work, we presented the **Transformer**, the first sequence transduction model based entirely on attention, replacing the recurrent layers most commonly used in encoder-decoder architectures with multi-headed self-attention.

For translation tasks, the Transformer can be trained **significantly faster** than architectures based on recurrent or convolutional layers. On both WMT 2014 English-to-German and English-to-French translation tasks, we achieve a **new state of the art**. In the former task our best model outperforms even all previously reported ensembles.

We are excited about the future of attention-based models and plan to apply them to other tasks. We plan to extend the Transformer to problems involving input and output modalities other than text and to investigate local, restricted attention mechanisms to efficiently handle large inputs and outputs such as images, audio, and video. Making generation less sequential is another research goal of ours.

---

## References

| # | Authors | Title | Year |
|---|---------|-------|------|
| [1] | Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E Hinton | Layer normalization | 2016 |
| [2] | Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio | Neural machine translation by jointly learning to align and translate | 2014 |
| [3] | Denny Britz, Anna Goldie, Minh-Thang Luong, Quoc V. Le | Massive exploration of neural machine translation architectures | 2017 |
| [4] | Jianpeng Cheng, Li Dong, Mirella Lapata | Long short-term memory-networks for machine reading | 2016 |
| [5] | Kyunghyun Cho et al. | Learning phrase representations using RNN encoder-decoder for statistical machine translation | 2014 |
| [6] | Francois Chollet | Xception: Deep learning with depthwise separable convolutions | 2016 |
| [7] | Junyoung Chung et al. | Empirical evaluation of gated recurrent neural networks on sequence modeling | 2014 |
| [8] | Chris Dyer et al. | Recurrent neural network grammars | 2016 |
| [9] | Jonas Gehring et al. | Convolutional sequence to sequence learning | 2017 |
| [10] | Alex Graves | Generating sequences with recurrent neural networks | 2013 |
| [11] | Kaiming He et al. | Deep residual learning for image recognition | 2016 |
| [12] | Sepp Hochreiter et al. | Gradient flow in recurrent nets: the difficulty of learning long-term dependencies | 2001 |
| [13] | Sepp Hochreiter, Jürgen Schmidhuber | Long short-term memory | 1997 |
| [14] | Zhongqiang Huang, Mary Harper | Self-training PCFG grammars with latent annotations across languages | 2009 |
| [15] | Rafal Jozefowicz et al. | Exploring the limits of language modeling | 2016 |
| [16] | Łukasz Kaiser, Samy Bengio | Can active memory replace attention? | 2016 |
| [17] | Łukasz Kaiser, Ilya Sutskever | Neural GPUs learn algorithms | 2016 |
| [18] | Nal Kalchbrenner et al. | Neural machine translation in linear time | 2017 |
| [19] | Yoon Kim et al. | Structured attention networks | 2017 |
| [20] | Diederik Kingma, Jimmy Ba | Adam: A method for stochastic optimization | 2015 |
| [21] | Oleksii Kuchaiev, Boris Ginsburg | Factorization tricks for LSTM networks | 2017 |
| [22] | Zhouhan Lin et al. | A structured self-attentive sentence embedding | 2017 |
| [23] | Minh-Thang Luong et al. | Multi-task sequence to sequence learning | 2015 |
| [24] | Minh-Thang Luong et al. | Effective approaches to attention-based neural machine translation | 2015 |
| [25] | Mitchell P Marcus et al. | Building a large annotated corpus of English: The Penn Treebank | 1993 |
| [26] | David McClosky et al. | Effective self-training for parsing | 2006 |
| [27] | Ankur Parikh et al. | A decomposable attention model | 2016 |
| [28] | Romain Paulus et al. | A deep reinforced model for abstractive summarization | 2017 |
| [29] | Slav Petrov et al. | Learning accurate, compact, and interpretable tree annotation | 2006 |
| [30] | Ofir Press, Lior Wolf | Using the output embedding to improve language models | 2016 |
| [31] | Rico Sennrich et al. | Neural machine translation of rare words with subword units | 2015 |
| [32] | Noam Shazeer et al. | Outrageously large neural networks: The sparsely-gated mixture-of-experts layer | 2017 |
| [33] | Nitish Srivastava et al. | Dropout: a simple way to prevent neural networks from overfitting | 2014 |
| [34] | Sainbayar Sukhbaatar et al. | End-to-end memory networks | 2015 |
| [35] | Ilya Sutskever et al. | Sequence to sequence learning with neural networks | 2014 |
| [36] | Christian Szegedy et al. | Rethinking the inception architecture for computer vision | 2015 |
| [37] | Vinyals & Kaiser et al. | Grammar as a foreign language | 2015 |
| [38] | Yonghui Wu et al. | Google's neural machine translation system: Bridging the gap between human and machine translation | 2016 |
| [39] | Jie Zhou et al. | Deep recurrent models with fast-forward connections for neural machine translation | 2016 |
| [40] | Muhua Zhu et al. | Fast and accurate shift-reduce constituent parsing | 2013 |

---

## Attention Visualizations

<img src="assets/attention-fig3.png" alt="Figure 3: Encoder self-attention tracking long-distance dependencies" width="480" />

**Figure 3:** An example of attention in layer 5 of 6, in the encoder, tracking long-distance dependencies. Many of the attention heads attend to the distant dependencies of the verb "making", completing the phrase "making...more difficult". Only attention weights for the word "making" are shown. Different colors represent different attention heads.

<img src="assets/attention-fig4a.png" alt="Figure 4: Attention in anaphora resolution" width="480" />

**Figure 4:** Two attention heads, also in layer 5, apparently involved in **anaphora resolution**. Top: full attentions for head 5. Bottom: isolated attentions from the word "its" for attention heads 5 and 6. Note that the attentions are very sharp for this word.

<img src="assets/attention-fig5a.png" alt="Figure 5: Attention heads learning sentence structure" width="480" />

**Figure 5:** Many attention heads exhibit behaviors related to **sentence structure**. Two examples from different heads in layer 5 of the encoder. The heads clearly learned to perform different tasks.
