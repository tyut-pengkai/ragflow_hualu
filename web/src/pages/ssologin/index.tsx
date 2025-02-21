import React, { useEffect } from 'react';
import { useNavigate, useSearchParams } from 'umi';
import { message } from 'antd';
import userService from '@/services/user-service';
import authorizationUtil from '@/utils/authorization-util';

const SSOLoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  useEffect(() => {
    const autoLogin = async () => {
      const email = searchParams.get('email');
      
      if (!email) {
        message.error('邮箱参数缺失');
        return;
      }

      try {
        const res = await userService.ssoLogin({email});
        
        if (res?.data?.data?.access_token) {
          const token = res.data.data.access_token;
          // 保存token
          authorizationUtil.setAuthorization(token);
          message.success('登录成功');
          
          // 带着token跳转
          navigate('/search', {
            state: { token },
            replace: true 
          });
        } else {
          message.error('登录失败，请检查您的邮箱');
          navigate('/login');
        }
      } catch (error) {
        message.error('登录过程中发生错误');
        console.error('SSO Login Error:', error);
      }
    };

    // 页面加载时自动执行登录
    autoLogin();
  }, [navigate, searchParams]);

  // 返回空白页面
  return null;
};

export default SSOLoginPage;

// import React, { useState } from 'react';
// import { useNavigate } from 'umi';
// import { message } from 'antd';
// import userService from '@/services/user-service';
// import authorizationUtil from '@/utils/authorization-util';

// const SSOLoginPage: React.FC = () => {
//   const [email, setEmail] = useState('');
//   const navigate = useNavigate();

//   const handleSSOLogin = async (e: React.FormEvent) => {
//     e.preventDefault();
//     try {
//       const res = await userService.ssoLogin({email});
//       //debugger
//       // 假设后端返回 token 或用户信息
//       if (res?.data?.data?.access_token) {
//         const token = res.data.data.access_token;
//         // 保存token
//         authorizationUtil.setAuthorization(token);
//         message.success('登录成功');
        
//         // 带着token跳转
//         navigate('/knowledge', {
//           state: { token },
//           replace: true  // 替换当前历史记录
//         });
//       } else {
//         message.error('登录失败，请检查您的邮箱');
//       }
//     } catch (error) {
//       message.error('登录过程中发生错误');
//       console.error('SSO Login Error:', error);
//     }
//   };

//   return (
//     <div style={{ 
//       display: 'flex', 
//       flexDirection: 'column', 
//       alignItems: 'center', 
//       justifyContent: 'center', 
//       height: '100vh' 
//     }}>
//       <h2>单点登录</h2>
//       <form 
//         onSubmit={handleSSOLogin} 
//         style={{ 
//           display: 'flex', 
//           flexDirection: 'column', 
//           width: '300px' 
//         }}
//       >
//         <input 
//           type="text" 
//           value={email}
//           onChange={(e) => setEmail(e.target.value)}
//           placeholder="请输入您的邮箱"
//           required
//           style={{ 
//             margin: '10px 0', 
//             padding: '10px', 
//             borderRadius: '4px', 
//             border: '1px solid #d9d9d9' 
//           }}
//         />
//         <button 
//           type="submit" 
//           style={{ 
//             margin: '10px 0', 
//             padding: '10px', 
//             backgroundColor: '#1890ff', 
//             color: 'white', 
//             border: 'none', 
//             borderRadius: '4px', 
//             cursor: 'pointer' 
//           }}
//         >
//           登录
//         </button>
//       </form>
//     </div>
//   );
// };

// export default SSOLoginPage;