# Data Selection

Choosing which channels to include in order to obtain a meaningful dataset comes with many considerations. The process and reasoning behind it is outlined below.

## Niches
There are 3 high-volume niche's being analyzed in this study: Gaming, Business and Technology.

Within each niche, I'm seperating them by channel size (small/medium/large) because ... (TODO)

| Size | Subscibers | Count per niche |
| :--- | :---: | ---: |
| Small | < 100k | 7
| Medium | 100k to 1M | 7
| Large | > 1M | 7

>Note: Count per niche subject to change (TBD)

## Consistent Uploader
Channels with consistent uploads are required. It ensures the following
1. **Enough videos per channel** - I want to compare relative performance, a video's views against the channel's own median. Not enough uploads will cause insignificant results.
2. **Stable baseline** - If a channel posted often in 2024, vanished, and then came back in 2026, I am comparing a 2026 video to 2024 median. That is effectively a different channel wearing the same name.
3. **One-hit wonders** - A channel with few videos and many subscribers indicates ***one*** of their vidoes went viral. It's median is meaningless and the channel is an outlier.

Therefore I will define an **"Consistent Uploader"** as
>**Consistent Uploader:** One who has posted at least 18 long-form videos in the past 18 months, with no large gaps in uploads
and only select channels who are consistent uploaders.

## Genre Spread within niche's
### Gaming
If all gaming channels cover the same game, say Minecraft, then any gaming vs tech or gaming vs business differences I find might be Minecraft vs tech or Minecraft vs business differences. There would be no way to tell them apart.

If all gaming channels cover different games, then I have zero ability to check whether game choice mattered.

| Channels per game | 3-4 |
| :--- | ---: |

>Note: channels per game subject to change (TBD)

#### Exclusion criteria
The following types of channels will not be considered
1. **Shorts-dominatied channels** 
2. **Stream VOD dumps** - unedited multi-hour uploads posted as an archive
3. **Clip/Compilation farms** - reuploaded content from other creators
4. **Dormant channels** - see "Consistent Uploader" above
5. **Non-English channels**
6. **Hidden subscribor counts**

### Business

TODO

### Technology

TODO

## Limitations
TODO
