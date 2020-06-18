<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Home</router-link> |
      <router-link to="/about"> About </router-link> |
      <router-link to="/logform"> Login </router-link> |
      <router-link to="/usertable"> User List </router-link> |
      <router-link to="/register"> Add Users </router-link> |
      <router-link to="/userupd"> Modify User </router-link> |
      <router-link to="/courseupd"> Modify Course </router-link> |
      <router-link to="/addcourse"> Add Course </router-link> |
      <router-link to="/coursetable"> Course List </router-link>

    </div>
    <router-view/>
  </div>
</template>

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
