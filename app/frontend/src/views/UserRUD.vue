<template>
    <UserRecord :users='users' @updrec='updaterec' @delrec='deleterec'> </UserRecord>
</template>
<script>
// @ is an alias to /src
import axios from 'axios';
import UserRecord from '../components/RUDUser.vue';

export default {
  name: 'UserTable',
  props: {
    users: Array,
  },
  components: {
    UserRecord,
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
    updaterec(userdat) {
      if (this.$store.getters.isAuthenticated) {
        this.$router.push({ name: 'UserModify', params: { user: userdat } });
      }
      else {
        alert("Session expired. You have to login again");
        this.logout();
      }
    },
    deleterec(userdat) {
      if (this.$store.getters.isAuthenticated) {
        const path = 'users/delete_log_json';
        if (this.$store.state.user === userdat.username) {
          alert("Can't delete this user as currently logged in by the same");
        }
        else {
          this.$store.dispatch('authrequest', { url: path, data: userdat.username })
            .then((response) => {
              alert(response.data.result);
              this.getUsers();
            })
            .catch((error) => {
              alert(error.response.data.result);
              console.error(error);
            });
        }
      }
      else {
        alert("Session expired. You have to login again");
        this.logout();
      }
    },
    getUsers() {
      const path = 'users/check_user_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((response) => {
          this.users = response.data.records;
          if (this.$store.state.userrole === 'Admin') {
            for (let i = 0; i < this.users.length; i += 1) {
              this.users[i].actions = '';
            }
          }
        })
        .catch((error) => {
          alert(error);
          console.error(error);
        });
    },
  },
  created() {
    if (this.$store.getters.isAuthenticated) {
      this.getUsers();
    }    
    else {      
      alert("Session expired. You have to login again");
      this.logout();
    }
  },
};
</script>
