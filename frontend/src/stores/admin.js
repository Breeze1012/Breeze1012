import { defineStore } from "pinia";
import http from "../api/http";

export const useAdminStore = defineStore("admin", {
  state: () => ({
    token: localStorage.getItem("admin_token") || "",
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(password) {
      const { data } = await http.post("/admin/login", { password });
      this.token = data.access_token;
      localStorage.setItem("admin_token", data.access_token);
    },
    logout() {
      this.token = "";
      localStorage.removeItem("admin_token");
    },
  },
});
