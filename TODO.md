# To do

* Docstrings, docs
* Datetime & pendulum matchers
* User [wrap_matcher()](https://pyhamcrest.readthedocs.io/en/release-1.8/helpers/#module-hamcrest.core.helpers.wrap_matcher) rather than the if isinstance stuff we do now.
* Write and use DiagnosingMatcher (similar to Java's [TypeSafeDiagnosingMatcher](http://hamcrest.org/JavaHamcrest/javadoc/1.3/org/hamcrest/TypeSafeDiagnosingMatcher.html))
* Is it possible to reuse py.test's string (or object) comparison code? It produces lovely diffs when you have 2 strings to compare.
