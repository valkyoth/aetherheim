//! Allocation-free bounds for untrusted byte and text inputs.

#![no_std]
#![forbid(unsafe_code)]

/// Error returned when an input exceeds its explicit bound.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct LimitExceeded {
    actual: usize,
    maximum: usize,
}

impl LimitExceeded {
    /// Returns the observed input length.
    #[must_use]
    pub const fn actual(self) -> usize {
        self.actual
    }

    /// Returns the admitted maximum length.
    #[must_use]
    pub const fn maximum(self) -> usize {
        self.maximum
    }
}

/// A borrowed byte slice admitted under a compile-time length ceiling.
#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub struct BoundedBytes<'a, const MAX: usize> {
    bytes: &'a [u8],
}

impl<'a, const MAX: usize> BoundedBytes<'a, MAX> {
    /// Validates and wraps a borrowed byte slice.
    pub const fn new(bytes: &'a [u8]) -> Result<Self, LimitExceeded> {
        if bytes.len() > MAX {
            return Err(LimitExceeded {
                actual: bytes.len(),
                maximum: MAX,
            });
        }
        Ok(Self { bytes })
    }

    /// Returns the validated bytes.
    #[must_use]
    pub const fn as_slice(self) -> &'a [u8] {
        self.bytes
    }

    /// Returns the validated byte length.
    #[must_use]
    pub const fn len(self) -> usize {
        self.bytes.len()
    }

    /// Reports whether the validated value is empty.
    #[must_use]
    pub const fn is_empty(self) -> bool {
        self.bytes.is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::BoundedBytes;

    #[test]
    fn exact_limit_is_accepted() {
        let value = BoundedBytes::<3>::new(b"cms");
        assert_eq!(value.map(BoundedBytes::len), Ok(3));
    }

    #[test]
    fn oversized_input_reports_both_lengths() {
        let error = BoundedBytes::<2>::new(b"cms");
        assert_eq!(
            error.map(BoundedBytes::len),
            Err(super::LimitExceeded {
                actual: 3,
                maximum: 2
            })
        );
    }

    #[test]
    fn empty_input_is_supported() {
        let value = BoundedBytes::<0>::new(b"");
        assert_eq!(value.map(BoundedBytes::is_empty), Ok(true));
    }
}
