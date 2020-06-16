<template>
  <div class="home">
    <ModifyUser :userrec = 'user' :depts = 'depts' :roles = 'roles'
    @userupd='updaterec'> </ModifyUser>
  </div>

</template>

<script>
// @ is an alias to /src
import ModifyUser from '@/components/ModifyUser.vue';

export default {
  name: 'UserModify',
  props: {
    user: Array,
    depts: Array,
    roles: Array,
  },
  components: {
    ModifyUser,
  },
  methods: {
    updaterec(userdat) {
      alert(userdat);
    },
  },
};
</script>
