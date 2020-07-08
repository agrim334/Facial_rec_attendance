<template>
  <div id="app">
    <div id = "nav" v-if="isAuth">
      <div id="nav" v-if="this.$store.state.userrole === 'Admin'">
        <router-link to="/">Home</router-link> |
        <router-link to="/usertable"> User List </router-link> |
        <router-link to="/register"> Add Users </router-link> |
        <router-link to="/addcourse"> Add Course </router-link> |
        <router-link to="/coursetable"> Course List </router-link>
        <router-link to="/adddept"> Add Department </router-link> |
        <router-link to="/depttable"> Department List </router-link>
        <router-link to="/addattd"> Mark Attendance </router-link> |
        <router-link to="/attdtable"> Attendance List </router-link>
        <router-link to="/addmap"> Add Mapping </router-link> |
        <router-link to="/maptable"> Mapping List </router-link>
        <router-link to="/pwdchg"> Change Password </router-link>
        <b-button @click='logout'> Logout </b-button>
        <router-view/>
      </div>
       <div id="nav" v-else-if="this.$store.state.userrole === 'TA'
       || this.$store.state.userrole === 'Prof'">
        <router-link to="/">Home</router-link> |
        <router-link to="/usertable"> User List </router-link> |
        <router-link to="/coursetable"> Course List </router-link>
        <router-link to="/depttable"> Department List </router-link>
        <router-link to="/addattd"> Mark Attendance </router-link> |
        <router-link to="/attdtable"> Attendance List </router-link>
        <router-link to="/maptable"> Mapping List </router-link>
        <router-link to="/pwdchg"> Change Password </router-link>
        <b-button @click='logout'> Logout </b-button>
        <router-view/>
      </div>
      <div id="nav" v-else-if="this.$store.state.userrole === 'Student'">
        <router-link to="/">Home</router-link> |
        <router-link to="/usertable"> User List </router-link> |
        <router-link to="/coursetable"> Course List </router-link>
        <router-link to="/depttable"> Department List </router-link>
        <router-link to="/attdtable"> Attendance List </router-link>
        <router-link to="/maptable"> Mapping List </router-link>
        <router-link to="/pwdchg"> Change Password </router-link>
        <b-button @click='logout'> Logout </b-button>
        <router-view/>
      </div>
    </div>
    <div id="nav" v-else>
      <router-link to="/login"> Login </router-link> |
      <router-link to="/resetreq"> Send Reset Request </router-link>
      <router-view/>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    isAuth() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
