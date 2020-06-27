<template>
 <div>
    {{ attd.cid }}
    {{ attd.sid }}
    {{ attd.fid }}
    {{ attd.taid }}
    {{ attd.time }}
    <button @click="deleterec"> Delete </button>
    <button @click="updaterec"> Update </button>
 </div>
</template>

<script>
export default {
  name: 'AttdRecord',
  props: { attd: Array },
  methods: {
    updaterec() {
      this.$emit('updrec', this.attd);
    },
    deleterec() {
      this.$emit('delrec', this.attd);
    },
  },
};
</script>
