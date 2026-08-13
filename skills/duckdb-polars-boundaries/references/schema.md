# Schema transfer

Check signedness, decimal precision/scale, timestamp unit/timezone, duration,
categorical/dictionary, nested list/struct/map, nullability, chunking, and column
order. Use an explicit cast at the owning stage when the consumer contract is
narrower. Parquet/Arrow metadata can preserve more than Python row objects.
