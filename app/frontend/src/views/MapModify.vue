<template>
  <div class="home">
    <ModifyMapForm :maprec = 'map' :roles = 'roles'
    @mapupd='updaterec'> </ModifyMapForm>
  </div>

</template>

<script>
// @ is an alias to /src
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
      alert(mapdat);
    },
  },
};
</script>
