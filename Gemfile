source "https://rubygems.org"

# Jekyll version compatible with GitHub Pages
# GitHub Pages uses Jekyll 4.3.x, so we match that
gem "jekyll", "~> 4.3"

# GitHub Pages compatible plugins
gem "jekyll-feed", "~> 0.12"
gem "jekyll-seo-tag", "~> 2.8"
gem "jekyll-sitemap", "~> 1.4"

# Note: jekyll-sass-converter is included automatically by GitHub Pages
# but explicitly listing it can help with local builds

# Windows não suporta alguns gems
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance e cache
gem "wdm", ">= 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
