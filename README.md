# Model_Efficiency
Calculate Model Efficiency, Study, Design Efficient Models

# To do
1. Calculate inference time of different models both on GPU and CPU, including MobileNet, ShuffleNet, AlexNet, SquezeeNet, ResNet etc.
2. Calculate inference time of different types of conv layer such as ResNet Bottleneck, SquezeeNet fire modules, AlexNet traditional modules, MobileNet 1x1 depthwise conv.
3. Combine different modules into a new model, this new model not only has high efficiency, but also has a competitive Accuracy.

* 1x1 depthwise conv: Feature fusion.
* channel shuffle: Feature fusion.
* Bottleneck: fast convergence and great generalization.
