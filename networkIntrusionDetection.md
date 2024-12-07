# 网络入侵检测

>目标是利用网络连接的数值型数据，构建一个<u>**入侵检测分类模型**</u>，用于识别网络入侵行为。
>
>通过**<u>机器学习算法及时检测潜在的异常连接</u>**，可以帮助企业主动预防和应对网络安全威胁，从而提高网络环境的安全性和稳定性。

## Dataset Process

### Dataset Describe

>[数据集](http://kdd.ics.uci.edu/databases/kddcup99/kddcup99.html)包含了多种网络连接记录的数值型特征，**每条记录标注为正常或异常（入侵）**，用于模型训练和评估。
>
>特征包括连接的<u>持续时间（duration）</u>、<u>协议类型（protocol_type，如TCP、UDP）</u>、<u>源到目标的数据字节数（src_bytes）</u>、<u>目标到源的数据字节数（dst_bytes）</u>等
>
>* 有标注信息
>* 总共label 5个大类，22个小类

### Features Describe

#### **表 1：单个TCP 连接的基本特征**

| 特征名称       | 描述                                          | 类型   |
| -------------- | --------------------------------------------- | ------ |
| duration       | 连接的时长（秒数）                            | 连续型 |
| protocol_type  | 协议类型，例如 tcp、udp 等                    | 离散型 |
| service        | 目标的网络服务，例如 http、telnet 等          | 离散型 |
| src_bytes      | 从源端发送到目标的数据字节数                  | 连续型 |
| dst_bytes      | 从目标接收的数据字节数                        | 连续型 |
| flag           | 连接状态（正常或错误状态）                    | 离散型 |
| land           | 如果连接是来自相同主机/端口，则为 1，否则为 0 | 离散型 |
| wrong_fragment | 错误的分段数量                                | 连续型 |
| urgent         | 紧急数据包的数量                              | 连续型 |

#### **表 2：Content features within a connection suggested by domain knowledge.**

| 特征名称           | 描述                                      | 类型   |
| ------------------ | ----------------------------------------- | ------ |
| hot                | “热”指标的数量                            | 连续型 |
| num_failed_logins  | 登录失败的尝试次数                        | 连续型 |
| logged_in          | 如果登录成功则为 1，否则为 0              | 离散型 |
| num_compromised    | “受损”条件的数量                          | 连续型 |
| root_shell         | 如果获得 root shell 权限则为 1，否则为 0  | 离散型 |
| su_attempted       | 如果尝试了 `su root` 命令则为 1，否则为 0 | 离散型 |
| num_root           | 使用 root 权限的操作数量                  | 连续型 |
| num_file_creations | 创建文件的操作次数                        | 连续型 |
| num_shells         | shell 提示符的数量                        | 连续型 |
| num_access_files   | 对访问控制文件的操作次数                  | 连续型 |
| num_outbound_cmds  | FTP 会话中的出站命令数                    | 连续型 |
| is_hot_login       | 如果登录属于“热”列表，则为 1，否则为 0    | 离散型 |
| is_guest_login     | 如果登录是“访客”登录，则为 1，否则为 0    | 离散型 |

#### 表3：Traffic features computed using a two-second time window.

| 特征名称                                     | 描述                                       | 类型   |
| -------------------------------------------- | ------------------------------------------ | ------ |
| count                                        | 在过去两秒内与当前连接到相同主机的连接数量 | 连续型 |
| **注意：以下特征与这些同一主机的连接有关。** |                                            |        |
| serror_rate                                  | 出现“SYN”错误的连接百分比                  | 连续型 |
| rerror_rate                                  | 出现“REJ”错误的连接百分比                  | 连续型 |
| same_srv_rate                                | 使用相同服务的连接百分比                   | 连续型 |
| diff_srv_rate                                | 使用不同服务的连接百分比                   | 连续型 |
| srv_count                                    | 在过去两秒内与当前连接到相同服务的连接数量 | 连续型 |
| **注意：以下特征与这些同一服务的连接有关。** |                                            |        |
| srv_serror_rate                              | 出现“SYN”错误的连接百分比                  | 连续型 |
| srv_rerror_rate                              | 出现“REJ”错误的连接百分比                  | 连续型 |
| srv_diff_host_rate                           | 连接到不同主机的百分比                     | 连续型 |



### Dataset Process

#### 1. 特征数量过多，对每一类特征做相关性分析

##### 1.1 Content data 相关性分析

![correlation_Content](C:\Users\Xuliang5262001\Desktop\NetworkIntrusionDetection\picture\correlation_Content.png)

>* 缺失的两行`num_outbound_cmds`以及`is_host_login`均是零，**<u>考虑删除</u>**，全零向量没有任何意义
>
>* 相关性分析：
>
>  >* 删除高度相关特征
>  >
>  >| 9    | ~~hot~~             | is_guest_login   | 0.84 | Moderate (0.8-0.9) |
>  >| ---- | ------------------- | ---------------- | ---- | ------------------ |
>  >| 40   | ~~su_attempted~~    | num_root         | 0.7  | Low (0.7-0.8)      |
>  >| 28   | ~~num_compromised~~ | ~~su_attempted~~ | 0.7  | Low (0.7-0.8)      |
>  >| 29   | ~~num_compromised~~ | num_root         | 0.99 | High (0.9-1.0)     |
>  >
>  >对这些特征进行<u>裁剪冗余</u>
>  >
>  >删除`['su_attempted','num_compromised','hot']`
>  >
>  >保留`['is_guest_login','num_root']`
>  >
>  >总共11个特征，删除3个，<u>剩余8个</u>
>  >
>  >* 删除低相关性特征
>  >
>  >  | 32   | ~~num_compromised~~ | num_access_files | 0.41 | Very Low (<0.7) |
>  >  | ---- | ------------------- | ---------------- | ---- | --------------- |
>  >  | 43   | ~~su_attempted~~    | num_access_files | 0.32 | Very Low (<0.7) |
>  >  | 37   | root_shell          | num_shells       | 0.17 | Very Low (<0.7) |
>  >  | 38   | root_shell          | num_access_files | 0.15 | Very Low (<0.7) |
>  >  | 47   | num_root            | num_access_files | 0.41 | Very Low (<0.7) |
>  >  | 1    | ~~hot~~             | logged_in        | 0.11 | Very Low (<0.7) |
>  >  | 13   | num_failed_logins   | su_attempted     | 0.12 | Very Low (<0.7) |
>  >  | 27   | ~~num_compromised~~ | root_shell       | 0.26 | Very Low (<0.7) |
>  >
>  >  总共8个特征，未删除

##### 1.2 Single data 相关性分析

![correlation_single](C:\Users\Xuliang5262001\Desktop\NetworkIntrusionDetection\picture\correlation_single.png)

>* 去除高相关性特征
>
>  >| 9    | protocol_type | flag        | -0.48 | Very Low (<0.7) |
>  >| ---- | ------------- | ----------- | ----- | --------------- |
>  >| 15   | ~~service~~   | flag        | -0.73 | Very Low (<0.7) |
>  >| 8    | protocol_type | ~~service~~ | 0.74  | Low (0.7-0.8)   |
>  >
>  >删除`[service]`
>  >
>  >总共9个特征，删除一个，剩余8个

##### 1.3 SrcTraffic data 相关性分析

![correlation_SrcTraffic](C:\Users\Xuliang5262001\Desktop\NetworkIntrusionDetection\picture\correlation_SrcTraffic.png)

>* 去除高相关的特征
>
>  >| 8    | ~~srv_count~~   | serror_rate         | -0.53 | Very Low (<0.7) |
>  >| ---- | --------------- | ------------------- | ----- | --------------- |
>  >| 9    | ~~srv_count~~   | srv_serror_rate     | -0.53 | Very Low (<0.7) |
>  >| 18   | serror_rate     | ~~same_srv_rate~~   | -0.86 | Very Low (<0.7) |
>  >| 23   | srv_serror_rate | ~~same_srv_rate~~   | -0.86 | Very Low (<0.7) |
>  >| 26   | rerror_rate     | ~~srv_rerror_rate~~ | 0.99  | High (0.9-1.0)  |
>  >| 0    | ~~count~~       | srv_count           | 0.94  | High (0.9-1.0)  |
>  >| 12   | srv_count       | ~~same_srv_rate~~   | 0.62  | Very Low (<0.7) |
>  >
>  >删除`['srv_count','same_srv_rate','srv_rerror_rate','count']`
>  >
>  >总共9个特征，删除4个特征，剩余5个特征
>
>

##### 1.4 DstTraffic data 相关性分析

![correlation_DstTraffic](C:\Users\Xuliang5262001\Desktop\NetworkIntrusionDetection\picture\correlation_DstTraffic.png)

>* 去除高度相关
>
>  >| 31   | dst_host_same_src_port_rate | ~~dst_host_serror_rate~~     | -0.58 | Very  Low (<0.7) |
>  >| ---- | --------------------------- | ---------------------------- | ----- | ---------------- |
>  >| 32   | dst_host_same_src_port_rate | ~~dst_host_srv_serror_rate~~ | -0.58 | Very Low (<0.7)  |
>  >| 14   | ~~dst_host_srv_count~~      | ~~dst_host_srv_serror_rate~~ | -0.77 | Very Low (<0.7)  |
>  >| 13   | ~~dst_host_srv_count~~      | ~~dst_host_serror_rate~~     | -0.78 | Very Low (<0.7)  |
>  >| 21   | dst_host_same_srv_rate      | ~~dst_host_srv_serror_rate~~ | -0.8  | Very Low (<0.7)  |
>  >| 20   | dst_host_same_srv_rate      | ~~dst_host_serror_rate~~     | -0.8  | Very Low (<0.7)  |
>  >| 39   | ~~dst_host_serror_rate~~    | ~~dst_host_srv_serror_rate~~ | 1     | High  (0.9-1.0)  |
>  >| 44   | ~~dst_host_rerror_rate~~    | dst_host_srv_rerror_rate     | 0.98  | High (0.9-1.0)   |
>  >| 9    | ~~dst_host_srv_count~~      | dst_host_same_srv_rate       | 0.97  | High (0.9-1.0)   |
>  >| 11   | ~~dst_host_srv_count~~      | dst_host_same_src_port_rate  | 0.68  | Very Low (<0.7)  |
>  >| 18   | dst_host_same_srv_rate      | dst_host_same_src_port_rate  | 0.67  | Very Low (<0.7)  |
>  >
>  >删除`['dst_host_srv_count','dst_host_rerror_rate','dst_host_serror_rate','dst_host_srv_serror_rate']`
>  >
>  >总共10个特征，删除4个特征，剩余6个特征
>
>

##### 1.5 局部相关性分析总结

>总共41个特征，删除两个全零向量，删除12个特征，剩余27个特征
>
>

#### 2. 对删除后的特征进行总体相关性分析

 
