import { useQuery, useQueryClient } from '@tanstack/react-query';
import userService from '@/services/user-service';
import { IUserInfo } from '@/interfaces/database/user-setting';
import { ResponseType } from '@/interfaces/database/base';
import { useEffect } from 'react';

export const useUserInfo = () => {
  const queryClient = useQueryClient();
  
  // 使用 useEffect 预加载数据
  useEffect(() => {
    // 预取用户信息
    queryClient.prefetchQuery({
      queryKey: ['userInfo'],
      queryFn: fetchUserInfo,
    });
  }, [queryClient]);

  const fetchUserInfo = async () => {
    try {
      const response = await userService.user_info();
      
      
      if (response?.data?.code === 0 && response?.data?.data) {
        const userInfo = {
          ...response.data.data,
          is_superuser: Boolean(response.data.data.is_superuser)
        };
        return {
          data: {
            code: 0,
            data: userInfo,
            message: 'success',
            status: 200
          }
        };
      }
      
      return response;
    } catch (error) {
      console.error('Error fetching user info:', error);
      throw error;
    }
  };

  const { data: responseData, isLoading } = useQuery<{
    data: ResponseType<IUserInfo>;
  }>({
    queryKey: ['userInfo'],
    queryFn: fetchUserInfo,
    // 配置：
    staleTime: 3600000, // 数据30秒内认为是新鲜的
    cacheTime: 3600000, // 缓存1小时
    refetchOnWindowFocus: true, // 窗口获得焦点时重新获取
    refetchOnMount: 'always', // 组件每次挂载时都重新获取
    retry: 3, // 失败时重试3次
  });
  
  const is_superuser = responseData?.is_superuser;

  return { is_superuser, loading: isLoading };
};