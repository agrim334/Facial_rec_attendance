<template>
  <div class="home">
    <ModifyMapForm :maprec = 'map' :roles = 'roles'
    @mapupd='updaterec'> </ModifyMapForm>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import ModifyMapForm from '@/components/ModifyMap.vue';

export default {
  name: 'MapModify',
  props: {
    map: Array,
    roles: Array,
  },
  components: {
    ModifyMapForm,
  },
  methods: {
    updaterec(mapdat) {
      const path = 'http://localhost:5000/map/modify_map_json';
      axios.post(path, { old: this.dept, new: mapdat })
        .then(() => {
          console.log('done');
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getroles() {
      const path = 'http://localhost:5000/roles/check_role_json';
      axios.get(path)
        .then((res) => {
          this.roles = res.data.records;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getroles();
  },
};
</script>
