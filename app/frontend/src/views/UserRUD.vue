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
      alert(userdat);
    },
    deleterec(userdat) {
      alert(userdat);
    },
    addrec() {
      alert('sdcf');
    },
    getUsers() {
      const path = 'http://localhost:5000/users/check_user_json';
      console.log(path);
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
