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
import UserRecord from '@/components/UserRUD.vue';

export default {
  name: 'UserTable',
  props: {
    users: Array,
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
  },
};
</script>
