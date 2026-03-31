import { createRouter, createWebHistory } from "vue-router";
import { useAdminStore } from "../stores/admin";
import { useAuthStore } from "../stores/auth";
import AdminLoginView from "../views/AdminLoginView.vue";
import AdminView from "../views/AdminView.vue";
import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import WorkspaceView from "../views/WorkspaceView.vue";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    // 普通用户路由
    { path: "/login", name: "login", component: LoginView },
    { path: "/register", name: "register", component: RegisterView },
    { path: "/", name: "workspace", component: WorkspaceView, meta: { requiresAuth: true } },

    // 管理员路由
    { path: "/admin/login", name: "admin-login", component: AdminLoginView },
    { path: "/admin", name: "admin", component: AdminView, meta: { requiresAdmin: true } },
  ]
});

router.beforeEach((to) => {
  try {
    const authStore = useAuthStore();
    const adminStore = useAdminStore();
    if (to.meta.requiresAdmin) {
      if (!adminStore.token) return { name: "admin-login" };
      return true;
    }
    if (to.name === "admin-login" && adminStore.token) return { name: "admin" };
    if (to.meta.requiresAuth && !authStore.token) return { name: "login" };
    if ((to.name === "login" || to.name === "register") && authStore.token) return { name: "workspace" };
    return true;
  } catch(e) {
    console.error("路由守卫报错:", e);
    return true;
  }
});

export default router;
