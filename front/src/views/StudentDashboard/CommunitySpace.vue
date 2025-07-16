<template>
  <div class="community-space">
    <aside class="sidebar left-sidebar">
      <div class="user-profile-card">
        <img :src="currentUser.avatar" alt="User Avatar" class="avatar">
        <h3>{{ currentUser.name }}</h3>
        <p>@{{ currentUser.handle }}</p>
        <div class="stats">
          <div><strong>帖子</strong><span>{{ currentUser.stats.posts }}</span></div>
          <div><strong>关注</strong><span>{{ currentUser.stats.following }}</span></div>
          <div><strong>粉丝</strong><span>{{ currentUser.stats.followers }}</span></div>
        </div>
      </div>
      <nav class="main-nav">
        <a href="#" class="nav-item active"><i class="icon-home"></i> 首页</a>
        <a href="#" class="nav-item"><i class="icon-explore"></i> 发现</a>
        <a href="#" class="nav-item"><i class="icon-notifications"></i> 通知</a>
        <a href="#" class="nav-item"><i class="icon-messages"></i> 消息</a>
        <a href="#" class="nav-item"><i class="icon-bookmarks"></i> 收藏</a>
        <a href="#" class="nav-item"><i class="icon-profile"></i> 个人主页</a>
      </nav>
      <button class="new-post-btn">发布新帖</button>
    </aside>

    <main class="main-content">
      <header class="main-header">
        <h2>首页</h2>
      </header>
      <div class="create-post-card">
        <textarea v-model="newPostText" placeholder="有什么新鲜事想分享？"></textarea>
        <div class="actions">
          <div class="media-buttons">
            <button><i class="icon-image"></i></button>
            <button><i class="icon-gif"></i></button>
            <button><i class="icon-poll"></i></button>
            <button><i class="icon-emoji"></i></button>
          </div>
          <button class="submit-post-btn" @click="submitPost" :disabled="!newPostText">发布</button>
        </div>
      </div>

      <div class="post-feed">
        <div v-for="post in posts" :key="post.id" class="post-card">
          <div class="post-header">
            <img :src="post.user.avatar" alt="Avatar" class="post-avatar">
            <div>
              <span class="post-user-name">{{ post.user.name }}</span>
              <span class="post-user-handle">@{{ post.user.handle }}</span>
              <span class="post-timestamp">· {{ post.timestamp }}</span>
            </div>
          </div>
          <p class="post-content">{{ post.content }}</p>
          <img v-if="post.image" :src="post.image" alt="Post image" class="post-image">
          <div class="post-actions">
            <button @click="toggleLike(post)">
              <i :class="['icon-comment', post.liked ? 'liked' : '']"></i> {{ post.stats.comments }}
            </button>
            <button @click="toggleLike(post)">
              <i :class="['icon-retweet', post.retweeted ? 'retweeted' : '']"></i> {{ post.stats.retweets }}
            </button>
            <button @click="toggleLike(post)">
              <i :class="['icon-like', post.liked ? 'liked' : '']"></i> {{ post.stats.likes }}
            </button>
            <button><i class="icon-share"></i></button>
          </div>
        </div>
      </div>
    </main>

    <aside class="sidebar right-sidebar">
       <div class="search-bar-card">
         <i class="icon-search"></i>
         <input type="text" placeholder="搜索...">
       </div>
       <div class="trends-card">
         <h3>热门话题</h3>
         <ul>
           <li v-for="trend in trends" :key="trend.topic">
             <div class="trend-info">
               <span>{{ trend.category }} · 趋势</span>
               <strong>#{{ trend.topic }}</strong>
               <span>{{ trend.posts }} 帖子</span>
             </div>
             <i class="icon-more"></i>
           </li>
         </ul>
       </div>
    </aside>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { getPosts, createPost, likePost, getTrends, getUserProfile } from '@/services/api.js';

export default {
  name: 'CommunitySpace',
  setup() {
    const newPostText = ref('');
    const posts = ref([]);
    const trends = ref([]);
    const currentUser = ref({
      id: 1,
      name: '加载中...',
      handle: 'loading',
      avatar: '/images/avatar.jpg',
      stats: {
        posts: 0,
        following: 0,
        followers: 0
      }
    });

    const fetchPosts = async () => {
      try {
        const response = await getPosts();
        posts.value = response.data;
      } catch (error) {
        console.error('获取帖子失败:', error);
      }
    };

    const fetchTrends = async () => {
      try {
        const response = await getTrends();
        trends.value = response.data;
      } catch (error) {
        console.error('获取热门话题失败:', error);
      }
    };

    const fetchCurrentUser = async () => {
      try {
        // 从 localStorage 获取当前登录的用户名
        const currentUsername = localStorage.getItem('username');
        if (!currentUsername) {
          console.error('未找到登录用户信息');
          return;
        }

        // 从 localStorage 获取所有用户信息
        const users = JSON.parse(localStorage.getItem('users') || '[]');
        const user = users.find(u => u.username === currentUsername);
        
        // 获取用户的个人资料信息（包括头像）
        const userProfileKey = `userProfile_${currentUsername}`;
        const userProfile = JSON.parse(localStorage.getItem(userProfileKey) || '{}');
        
        if (user) {
          currentUser.value = {
            id: user.id || Date.now(), // 如果没有id，使用时间戳作为临时id
            name: user.username, // 使用用户名作为显示名称
            handle: user.username,
            avatar: userProfile.avatar || user.avatar || '/images/avatar.jpg', // 优先使用个人资料中的头像
            stats: {
              posts: user.postsCount || 0,
              following: user.followingCount || 0,
              followers: user.followersCount || 0
            }
          };
        } else {
          // 如果在本地存储中找不到用户，尝试调用API
          const response = await getUserProfile(currentUsername);
          currentUser.value = {
            ...response.data,
            stats: {
              posts: response.data.postsCount || 0,
              following: response.data.followingCount || 0,
              followers: response.data.followersCount || 0
            }
          };
        }
      } catch (error) {
        console.error('获取用户信息失败:', error);
        // 如果所有方法都失败，使用当前登录的用户名作为默认值
        const currentUsername = localStorage.getItem('username') || '未知用户';
        currentUser.value = {
          id: Date.now(),
          name: currentUsername,
          handle: currentUsername,
          avatar: '/images/avatar.jpg',
          stats: {
            posts: 0,
            following: 0,
            followers: 0
          }
        };
      }
    };

    const submitPost = async () => {
      if (!newPostText.value.trim()) return;
      try {
        const newPostData = { content: newPostText.value, userId: currentUser.value.id };
        const response = await createPost(newPostData);
        posts.value.unshift(response.data);
        newPostText.value = '';
      } catch (error) {
        console.error('发布帖子失败:', error);
      }
    };

    const toggleLike = async (post) => {
      try {
        await likePost(post.id);
        post.liked = !post.liked;
        post.stats.likes += post.liked ? 1 : -1;
      } catch (error) {
        console.error('点赞失败:', error);
      }
    };

    onMounted(() => {
      fetchCurrentUser();
      fetchPosts();
      fetchTrends();
    });

    return {
      newPostText,
      posts,
      trends,
      currentUser,
      submitPost,
      toggleLike,
    };
  },
};
</script>

<style scoped>
/* Basic Layout */
.community-space {
  display: flex;
  justify-content: center;
  width: 100%;
  min-height: 100vh;
  background-color: #f0f2f5;
  color: #333;
}

.sidebar { flex-shrink: 0; padding: 1.5rem; }
.left-sidebar { width: 280px; }
.right-sidebar { width: 320px; }
.main-content { width: 600px; border-left: 1px solid #e6ecf0; border-right: 1px solid #e6ecf0; }

/* Cards */
.user-profile-card, .create-post-card, .post-card, .trends-card, .search-bar-card {
  background-color: #fff;
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

/* Left Sidebar */
.user-profile-card { text-align: center; }
.user-profile-card .avatar { width: 80px; height: 80px; border-radius: 50%; margin-bottom: 1rem; }
.user-profile-card h3 { margin: 0; font-size: 1.2rem; }
.user-profile-card p { color: #657786; margin: 0.2rem 0 1rem; }
.user-profile-card .stats { display: flex; justify-content: space-around; }
.user-profile-card .stats div { display: flex; flex-direction: column; }
.user-profile-card .stats span { color: #657786; font-size: 0.9rem; }

.main-nav .nav-item { display: flex; align-items: center; padding: 1rem; font-size: 1.1rem; font-weight: 500; border-radius: 99px; transition: background-color 0.2s; }
.main-nav .nav-item:hover { background-color: #e8f5fe; color: #1da1f2; }
.main-nav .nav-item.active { color: #1da1f2; font-weight: 700; }
.main-nav .nav-item i { margin-right: 1rem; }

.new-post-btn { width: 100%; padding: 1rem; background-color: #1da1f2; color: white; border: none; border-radius: 99px; font-size: 1.1rem; font-weight: 700; cursor: pointer; transition: background-color 0.2s; }
.new-post-btn:hover { background-color: #0c85d0; }

/* Main Content */
.main-header { padding: 1rem 1.5rem; border-bottom: 1px solid #e6ecf0; }
.main-header h2 { margin: 0; font-size: 1.2rem; }

.create-post-card textarea { width: 100%; border: none; resize: none; font-size: 1.1rem; min-height: 60px; outline: none; }
.create-post-card .actions { display: flex; justify-content: space-between; align-items: center; margin-top: 1rem; }
.media-buttons button { background: none; border: none; color: #1da1f2; font-size: 1.2rem; cursor: pointer; padding: 0.5rem; }
.submit-post-btn { background-color: #1da1f2; color: white; border: none; border-radius: 99px; padding: 0.5rem 1.5rem; font-weight: 700; cursor: pointer; }
.submit-post-btn:disabled { background-color: #a5d8f8; cursor: not-allowed; }

.post-card { padding: 1rem 1.5rem; border-bottom: 1px solid #e6ecf0; transition: background-color 0.2s; }
.post-card:hover { background-color: #fafafa; }
.post-header { display: flex; align-items: center; margin-bottom: 0.5rem; }
.post-avatar { width: 48px; height: 48px; border-radius: 50%; margin-right: 1rem; }
.post-user-name { font-weight: 700; }
.post-user-handle, .post-timestamp { color: #657786; margin-left: 0.5rem; }
.post-content { margin: 0.5rem 0; line-height: 1.5; }
.post-image { width: 100%; border-radius: 16px; margin-top: 1rem; }
.post-actions { display: flex; justify-content: space-around; margin-top: 1rem; color: #657786; }
.post-actions button { background: none; border: none; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; }
.post-actions .liked { color: #e0245e; }
.post-actions .retweeted { color: #17bf63; }

/* Right Sidebar */
.search-bar-card { display: flex; align-items: center; padding: 0.8rem 1.5rem; }
.search-bar-card input { border: none; outline: none; background: transparent; width: 100%; margin-left: 1rem; }

.trends-card h3 { font-size: 1.2rem; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #e6ecf0; }
.trends-card ul { list-style: none; padding: 0; }
.trends-card li { display: flex; justify-content: space-between; align-items: center; padding: 0.8rem 0; cursor: pointer; transition: background-color 0.2s; }
.trends-card li:hover { background-color: #f5f8fa; }
.trend-info span { font-size: 0.9rem; color: #657786; }
.trend-info strong { display: block; font-size: 1rem; margin: 0.2rem 0; }

/* Icons - Placeholder, you would use an icon library */
[class^="icon-"] { font-family: 'your-icon-font'; /* Replace with your icon font */ }
</style>