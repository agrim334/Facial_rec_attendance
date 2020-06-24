<template>
  <div class="home">
    <table>
      <tr v-for='user in users' :key='user.userid'>
        <UserRecord :user='user' @updrec='updaterec' @delrec='deleterec'></UserRecord>
      </tr>
    </table>
    <button id='add' @click='addrec'>Add Users</button>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import UserRecord from '@/components/RUDUser.vue';

export default {
  name: 'UserTable',
  data() {
    return {
      users: [],
    };
  },
  components: {
    UserRecord,
  },
  methods: {
    updaterec(userdat) {
      this.$router.push('userupd', { params: { user: userdat } });
    },
    deleterec(userdat) {
      const path = 'http://localhost:5000/users/delete_log_json';
      console.log(userdat.username);
      axios.post(path, userdat.username)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    addrec() {
      alert('sdcf');
    },
    getUsers() {
      const path = 'http://localhost:5000/users/check_user_json';
      axios.get(path)
        .then((res) => {
          this.users = res.data.records;
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
