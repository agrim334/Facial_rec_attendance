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
    updaterec(userdat) {
      this.$router.push({ name: 'UserModify', params: { user: userdat } });
    },
    deleterec(userdat) {
      const path = 'http://localhost:5000/users/delete_log_json';
      this.$store.dispatch('authrequest', { url: path, data: userdat.username })
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getUsers() {
      const path = 'http://localhost:5000/users/check_user_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((res) => {
          this.users = res.data.records;
          for (let i = 0; i < this.users.length; i += 1) {
            this.users[i].actions = '';
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getUsers();
  },
};
</script>
