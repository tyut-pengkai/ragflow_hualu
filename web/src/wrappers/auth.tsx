import { useAuth } from '@/hooks/auth-hooks';
import { useUserInfo } from '@/hooks/user-hooks';
import { Routes } from '@/routes';
import { Navigate, Outlet, useLocation } from 'umi';

// 需要超级用户权限的路由
const superUserRoutes = [
 '/knowledge',  // 知识库
  '/flow',     // Agent
  '/file',     // 文件管理
  '/user-setting/model', // 模型管理
  '/user-setting/api', // API管理
];

export default () => {
  const { isLogin } = useAuth();
  const { is_superuser, loading } = useUserInfo();
  const location = useLocation();

  if (isLogin === false) {
    return <Navigate to="/login" />;
  }
  //增加日志
  
  if (isLogin === true) {
    // 检查是否需要加载用户信息
    if (loading) {
      return null; // 或者显示加载状态
    }

    // 检查当前路由是否需要超级用户权限
    const needsSuperUser = superUserRoutes.some(route => 
      location.pathname.startsWith(route)
    );
    
    if (needsSuperUser && is_superuser !== true) {
      //提醒用户没权限
      alert('您没有权限访问该页面');
      return <Navigate to="/search" />;
    }

    return <Outlet />;
  }

  return null;
};
