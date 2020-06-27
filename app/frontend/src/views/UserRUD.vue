<template>
  <div class="home">
    <b-table :items='users'>
      <template v-slot:cell(actions)='row'>
        <b-button @click='deleterec'> Delete </b-button>
        <b-button @click='updaterec(row)'> Update </b-button>
      </template>
    </b-table>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';

export default {
  name: 'UserTable',
  data() {
    return {
      users: [],
    };
  },
  methods: {
    updaterec(userdat) {
      this.$router.push({ name: 'UserModify', params: { user: userdat.item } });
    },
    deleterec(userdat) {
      const path = 'http://localhost:5000/users/delete_log_json';
      axios.post(path, userdat.item.username)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getUsers() {
      const path = 'http://localhost:5000/users/check_user_json';
      axios.get(path)
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
