const { createApp } = Vue;

createApp({
    data() {
        return {
            categories: [],
            selectedCategory: null,
            commodities: [],
            searchQuery: ""
        };
    },

    computed: {
        filteredCommodities() {
            if (!this.searchQuery) return this.commodities;

            return this.commodities.filter(item =>
                item.commodity.toLowerCase().includes(this.searchQuery.toLowerCase())
            );
        }
    },

    methods: {

        async fetchCategories() {
            const res = await fetch("http://localhost:5000/categories");
            this.categories = await res.json();

            if (!this.selectedCategory && this.categories.length > 0) {
                this.selectedCategory = this.categories[0];
                await this.fetchCommodities();
            }
        },

        async fetchCommodities() {
            if (!this.selectedCategory) return;

            const res = await fetch(
                `http://localhost:5000/commodities?category=${encodeURIComponent(this.selectedCategory)}&limit=100`
            );

            const data = await res.json();
            this.commodities = data.data; // FULL RELOAD (important fix)
        },

        async selectCategory(cat) {
            this.selectedCategory = cat;
            this.commodities = []; // clear old data
            await this.fetchCommodities();
        }
    },

    mounted() {
        this.fetchCategories();

        setInterval(() => {
            this.fetchCommodities();
        }, 30000);
    }

}).mount("#app");