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
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
    updaterec(userdat) {
      if (this.isAuthenticated) {
        this.$router.push({ name: 'UserModify', params: { user: userdat } });
      }
      else{
        alert("Session expired. You have to login again");
        this.logout();
      }
    },
    deleterec(userdat) {
      const path = 'users/delete_log_json';
      if (this.$store.state.user === userdat.username) {
        alert("Can't delete this user as currently logged in by the same");
      }
      else {
        this.$store.dispatch('authrequest', { url: path, data: userdat.username })
          .then(() => {
            this.getUsers();
          })
          .catch((error) => {
            alert(error);
            console.error(error);
          });
      }
    },
    getUsers() {
      const path = 'users/check_user_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((res) => {
          if (res.data.message === 'Invalid token') {
            alert("Bad session logging out");
            this.logout();
          }
          if (res.data.message === 'Expired token') {
            alert("Session expired. You have to login again");
            this.logout();
          }
          this.users = res.data.records;
          if (this.$store.state.userrole === 'Admin') {
            for (let i = 0; i < this.users.length; i += 1) {
              this.users[i].actions = '';
            }
          }
        })
        .catch((error) => {
          alert(error);
          this.logout();
          console.error(error);
        });
    },
  },
  created() {
    this.getUsers();
  },
};
</script>
