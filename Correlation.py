import pandas as pd

# 手动录入从图中提取的相关性数据（示例）
data = {
    'dst_host_count': [1.0, -0.027, -0.13, 0.025, 0.29, -0.49, 0.16, 0.16, -0.092, -0.088],
    'dst_host_srv_count': [-0.027, 1.0, 0.97, -0.46, 0.68, -0.017, -0.78, -0.77, -0.33, -0.33],
    'dst_host_same_srv_rate': [-0.13, 0.97, 1.0, -0.47, 0.67, 0.058, -0.8, -0.8, -0.32, -0.32],
    'dst_host_diff_srv_rate': [0.025, -0.46, -0.47, 1.0, -0.16, 0.0063, 0.16, 0.16, 0.22, 0.21],
    'dst_host_same_src_port_rate': [0.29, 0.68, 0.67, -0.16, 1.0, -0.064, -0.58, -0.58, -0.27, -0.27],
    'dst_host_srv_diff_host_rate': [-0.49, -0.017, 0.058, 0.0063, -0.064, 1.0, -0.071, -0.072, 0.14, 0.14],
    'dst_host_serror_rate': [0.16, -0.78, -0.8, 0.16, -0.58, -0.071, 1.0, 1.0, -0.11, -0.11],
    'dst_host_srv_serror_rate': [0.16, -0.77, -0.8, 0.16, -0.58, -0.072, 1.0, 1.0, -0.11, -0.12],
    'dst_host_rerror_rate': [-0.092, -0.33, -0.32, 0.22, -0.27, 0.14, -0.11, -0.11, 1.0, 0.98],
    'dst_host_srv_rerror_rate': [-0.088, -0.33, -0.32, 0.21, -0.27, 0.14, -0.11, -0.12, 0.98, 1.0]
}

# 创建 DataFrame
correlation_df = pd.DataFrame(data, index=[
    'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
    'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
    'dst_host_srv_serror_rate', 'dst_host_rerror_rate', 'dst_host_srv_rerror_rate'
])
