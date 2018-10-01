@echo off

..\bin\xmlchain -anno data\smile -rest "no smile" -step 5 smile_features data\action_units data\smile
..\bin\xmltrain -out smile smile_template