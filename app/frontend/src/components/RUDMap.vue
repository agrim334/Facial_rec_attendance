<template>
 <div>
    {{ map.cid }}
    {{ map.uid }}
    {{ map.role }}
    <button @click="deleterec"> Delete </button>
    <button @click="updaterec"> Update </button>
 </div>
</template>

<script>
export default {
  name: 'MapRecord',
  props: {
    map: Array,
  },
  methods: {
    updaterec() {
      this.$emit('updrec', this.map);
    },
    deleterec() {
      this.$emit('delrec', this.map);
    },
  },
};
</script>
